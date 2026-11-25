import glob
import os
import sys

import click
import requests

from .core import (
    TOC_START_TAG,
    ExistingUnmanagedTocError,
    is_current,
    modify_and_write,
    render_diff,
)
from .markdown import MarkdownError, as_link, get_links, headers

REQUEST_TIMEOUT = 10


def _check_links(markdown_file, contents, on_invalid_link="warn"):
    verbose = on_invalid_link != "ignore"
    if verbose:
        click.echo(
            click.style(f"Checking hyperlinks in {markdown_file}...", fg="yellow"),
            color=True,
        )
    valid_http_fragments = {"#" + as_link(h) for (_, h) in headers(contents)}

    counts = {"valid": 0, "invalid": 0, "timeout": 0, "error": 0, "unrecognized": 0}

    for text, link, _, _ in get_links(contents):
        label = f"[{text}]({link})"
        if link.startswith("#"):
            ok = link in valid_http_fragments
            counts["valid" if ok else "invalid"] += 1
            if verbose:
                click.echo(
                    click.style(
                        f"{'VALID' if ok else 'INVALID'}: {label}",
                        fg="green" if ok else "red",
                    ),
                    color=True,
                )
        elif link.startswith("http://") or link.startswith("https://"):
            try:
                r = requests.get(link, timeout=REQUEST_TIMEOUT)
                ok = r.status_code < 400
            except requests.exceptions.Timeout:
                counts["timeout"] += 1
                if verbose:
                    click.echo(
                        click.style(f"TIMEOUT: {label}", fg="yellow"), color=True
                    )
                continue
            except requests.exceptions.RequestException as e:
                counts["error"] += 1
                if verbose:
                    click.echo(
                        click.style(f"ERROR: {label} ({e})", fg="red"), color=True
                    )
                continue
            counts["valid" if ok else "invalid"] += 1
            if verbose:
                status = f"{'VALID' if ok else 'INVALID'} ({r.status_code})"
                if r.history:
                    status += f" [redirected to {r.url}]"
                click.echo(
                    click.style(f"{status}: {label}", fg="green" if ok else "red"),
                    color=True,
                )
        else:
            counts["unrecognized"] += 1
            if verbose:
                click.echo(
                    click.style(f"UNRECOGNIZED LINK TYPE: {label}", fg="yellow"),
                    color=True,
                )

    if verbose:
        summary = ", ".join(f"{n} {cat}" for cat, n in counts.items() if n)
        if summary:
            click.echo(click.style(f"Summary: {summary}", fg="cyan"), color=True)

    return counts["invalid"] + counts["timeout"] + counts["error"] > 0


def _resolve_paths(patterns):
    paths = []
    for pattern in patterns:
        expanded = os.path.expanduser(pattern)
        matched = glob.glob(expanded, recursive=True)
        if matched:
            paths.extend(matched)
        else:
            paths.append(expanded)
    return paths


@click.command()
@click.argument("markdown_files", nargs=-1, required=True)
@click.option(
    "--outfile", "-o", help="Output file (only valid when processing a single file)."
)
@click.option(
    "--check-links", "-cl", is_flag=True, help="Check validity of hyperlinks."
)
@click.option("--title", "-t", default=None, help="Custom TOC title line.")
@click.option(
    "--max-depth",
    "-d",
    default=None,
    type=int,
    help="Maximum heading depth to include in TOC.",
)
@click.option(
    "--check",
    "-c",
    is_flag=True,
    help="Check whether the TOC is up to date without writing; exit non-zero if stale.",
)
@click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="Exclude headers whose text contains this value from the TOC "
    "(repeatable for multiple exclusions).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would change (as a unified diff) without writing any files. "
    "Works with multiple input files.",
)
@click.option(
    "--backup",
    is_flag=True,
    help="Back up each file to <file>.bak with its pre-modification content "
    "before writing.",
)
@click.option(
    "--after",
    "-a",
    default=None,
    help="On the first run (before TOC markers exist), insert the TOC block "
    "immediately after the first line containing this text, instead of at "
    "the top of the file. Ignored if no line matches, and has no effect on "
    "later runs, which always update the TOC in place.",
)
@click.option(
    "--wrap-existing",
    is_flag=True,
    help="If a hand-written 'Table of Contents'-style section (a heading "
    "followed by a list of links) is found with no doctoc markers, wrap it "
    "in doctoc's markers instead of refusing to write, so doctoc manages it "
    "on subsequent runs.",
)
@click.option(
    "--numbered",
    "-n",
    is_flag=True,
    help="Render TOC entries as a numbered list instead of bullets.",
)
@click.option(
    "--on-invalid-link",
    type=click.Choice(["ignore", "warn", "error"]),
    default="warn",
    help="How to handle invalid links found by --check-links: 'warn' (default) "
    "prints them but exits 0, 'error' prints them and exits non-zero if any "
    "link failed, 'ignore' suppresses link-check output entirely.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Print extra detail per file: header count found, whether an "
    "existing TOC block was updated or a new one inserted, and (with "
    "--check-links) how many links were checked.",
)
def main(
    markdown_files,
    outfile,
    check_links,
    title,
    max_depth,
    check,
    exclude,
    dry_run,
    backup,
    after,
    wrap_existing,
    numbered,
    on_invalid_link,
    verbose,
):
    """Generate or update a table of contents for one or more Markdown files.

    MARKDOWN_FILES may be file paths or glob patterns (e.g. '**/*.md').
    """
    paths = _resolve_paths(markdown_files)

    if outfile and len(paths) > 1:
        click.echo(
            click.style(
                "--outfile cannot be used with multiple input files.", fg="red"
            ),
            color=True,
        )
        sys.exit(1)

    had_error = False
    for path in paths:
        try:
            if check:
                if is_current(
                    path,
                    title=title,
                    max_depth=max_depth,
                    exclude=exclude,
                    after=after,
                    wrap_existing=wrap_existing,
                    numbered=numbered,
                ):
                    click.echo(click.style(f"OK: {path} is up to date", fg="green"))
                else:
                    click.echo(click.style(f"STALE: {path} is out of date", fg="red"))
                    had_error = True
                continue

            if dry_run:
                diff = render_diff(
                    path,
                    title=title,
                    max_depth=max_depth,
                    exclude=exclude,
                    after=after,
                    wrap_existing=wrap_existing,
                    numbered=numbered,
                )
                if diff:
                    click.echo(diff, nl=False)
                else:
                    click.echo(click.style(f"OK: {path} is up to date", fg="green"))
                continue

            if check_links or verbose:
                with open(path) as fp:
                    original_contents = fp.read()

            if verbose:
                header_count = len(list(headers(original_contents)))
                toc_status = (
                    "updated existing TOC block"
                    if TOC_START_TAG in original_contents
                    else "inserted new TOC block"
                )

            dest = modify_and_write(
                path,
                outfile=outfile,
                title=title,
                max_depth=max_depth,
                exclude=exclude,
                backup=backup,
                after=after,
                wrap_existing=wrap_existing,
                numbered=numbered,
            )
            click.echo(
                click.style(f"Success: wrote TOC to {dest}", fg="green"), color=True
            )

            if verbose:
                click.echo(
                    click.style(
                        f"  Headers found: {header_count}, {toc_status}", fg="cyan"
                    ),
                    color=True,
                )

            if check_links:
                if verbose:
                    link_count = len(list(get_links(original_contents)))
                    click.echo(
                        click.style(f"  Links checked: {link_count}", fg="cyan"),
                        color=True,
                    )
                any_failed = _check_links(
                    path, original_contents, on_invalid_link=on_invalid_link
                )
                if on_invalid_link == "error" and any_failed:
                    had_error = True

        except OSError as e:
            click.echo(click.style(f"Failed ({path}): {e}", fg="red"), color=True)
            had_error = True
        except MarkdownError as e:
            click.echo(click.style(f"Failed ({path}): {e}", fg="red"), color=True)
            had_error = True
        except ExistingUnmanagedTocError as e:
            click.echo(click.style(f"Skipped ({path}): {e}", fg="yellow"), color=True)
            had_error = True

    if had_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
