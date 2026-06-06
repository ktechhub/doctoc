import glob
import os
import sys

import click
import requests

from .core import modify_and_write
from .markdown import MarkdownError, as_link, get_links, headers

REQUEST_TIMEOUT = 10


def _check_links(markdown_file, contents):
    click.echo(click.style(f"Checking hyperlinks in {markdown_file}...", fg="yellow"), color=True)
    valid_http_fragments = {"#" + as_link(h) for (_, h) in headers(contents)}

    for text, link, _, _ in get_links(contents):
        label = f"[{text}]({link})"
        if link.startswith("#"):
            ok = link in valid_http_fragments
            click.echo(
                click.style(f"{'VALID' if ok else 'INVALID'}: {label}", fg="green" if ok else "red"),
                color=True,
            )
        elif link.startswith("http://") or link.startswith("https://"):
            try:
                r = requests.get(link, timeout=REQUEST_TIMEOUT)
                ok = r.status_code < 400
            except requests.exceptions.Timeout:
                click.echo(click.style(f"TIMEOUT: {label}", fg="yellow"), color=True)
                continue
            except requests.exceptions.RequestException as e:
                click.echo(click.style(f"ERROR: {label} ({e})", fg="red"), color=True)
                continue
            click.echo(
                click.style(f"{'VALID' if ok else 'INVALID'}: {label}", fg="green" if ok else "red"),
                color=True,
            )
        else:
            click.echo(click.style(f"UNRECOGNIZED LINK TYPE: {label}", fg="yellow"), color=True)


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
@click.option("--outfile", "-o", help="Output file (only valid when processing a single file).")
@click.option("--check-links", "-cl", is_flag=True, help="Check validity of hyperlinks.")
@click.option("--title", "-t", default=None, help="Custom TOC title line.")
@click.option("--max-depth", "-d", default=None, type=int, help="Maximum heading depth to include in TOC.")
def main(markdown_files, outfile, check_links, title, max_depth):
    """Generate or update a table of contents for one or more Markdown files.

    MARKDOWN_FILES may be file paths or glob patterns (e.g. '**/*.md').
    """
    paths = _resolve_paths(markdown_files)

    if outfile and len(paths) > 1:
        click.echo(
            click.style("--outfile cannot be used with multiple input files.", fg="red"),
            color=True,
        )
        sys.exit(1)

    had_error = False
    for path in paths:
        try:
            if check_links:
                with open(path) as fp:
                    original_contents = fp.read()

            dest = modify_and_write(path, outfile=outfile, title=title, max_depth=max_depth)
            click.echo(click.style(f"Success: wrote TOC to {dest}", fg="green"), color=True)

            if check_links:
                _check_links(path, original_contents)

        except OSError as e:
            click.echo(click.style(f"Failed ({path}): {e}", fg="red"), color=True)
            had_error = True
        except MarkdownError as e:
            click.echo(click.style(f"Failed ({path}): {e}", fg="red"), color=True)
            had_error = True

    if had_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
