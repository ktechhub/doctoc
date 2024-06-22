import click
import os, sys
import requests
from .core import modify_and_write
from .markdown import headers, get_links, as_link, MarkdownError


@click.command()
@click.argument("markdown_file")
@click.option("--outfile", "-o", help="Specify an output file instead of overwriting.")
@click.option(
    "--check-links", "-cl", is_flag=True, help="Check validity of hyperlinks."
)
def main(markdown_file, outfile, check_links):
    """
    Generate or update a table of contents for Markdown files and optionally check hyperlinks.

    Args:
        markdown_file (str): Path to the Markdown file to process.
        outfile (str, optional): Output file path. If specified, writes the modified content to this file instead of overwriting the original.
        check_links (bool): Flag to enable checking the validity of hyperlinks found in the Markdown file.
    """
    try:
        markdown_file = os.path.expanduser(markdown_file)
        modify_and_write(markdown_file, outfile)

        if check_links:
            click.echo(click.style("Checking hyperlinks...", fg="yellow"), color=True)
            with open(markdown_file) as fp:
                contents = fp.read()

            valid_http_fragments = ["#" + as_link(h) for (_, h) in headers(contents)]
            for text, link, _, _ in get_links(contents):
                if link.startswith("#"):
                    if link not in valid_http_fragments:
                        click.echo(
                            click.style(f"INVALID: [{text}]({link})", fg="red"),
                            color=True,
                        )
                    else:
                        click.echo(
                            click.style(f"VALID: [{text}]({link})", fg="green"),
                            color=True,
                        )
                elif link.startswith("http://") or link.startswith("https://"):
                    r = requests.get(link)
                    click.echo(
                        click.style(
                            f"{'VALID' if r.status_code == 200 else 'INVALID'}: [{text}]({link})",
                            fg="green" if r.status_code == 200 else "red",
                        ),
                        color=True,
                    )
                else:
                    click.echo(
                        click.style(
                            f"UNRECOGNIZED LINK TYPE: [{text}]({link})", fg="yellow"
                        ),
                        color=True,
                    )

    except OSError as e:
        click.echo(click.style(f"Failed: {e}", fg="red"), color=True)
        sys.exit(1)
    except MarkdownError as e:
        click.echo(click.style(f"Failed: {e}", fg="red"), color=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
