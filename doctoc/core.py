import click
from .markdown import toc

TOC_START_TAG = (
    "<!-- START doctoc generated TOC please keep comment here to allow auto update -->"
)
TOC_END_TAG = (
    "<!-- END doctoc generated TOC please keep comment here to allow auto update -->"
)


def modify_and_write(path, outfile=None):

    with open(path) as fp:
        markdown = fp.read()

    table_of_contents = toc(markdown)

    start_index = markdown.find(TOC_START_TAG)
    end_index = markdown.find(TOC_END_TAG) + len(TOC_END_TAG)

    if start_index != -1 and end_index != -1:
        new_markdown = (
            markdown[:start_index]
            + TOC_START_TAG
            + "\n\n"
            + f"**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*\n\n"
            + f"<!---toc start-->\n\n{table_of_contents}\n\n<!---toc end-->\n\n"
            + TOC_END_TAG
            + "\n"
            + markdown[end_index:]
        )
    else:
        new_markdown = (
            f"{TOC_START_TAG}\n"
            f"<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n"
            f"**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*\n\n"
            f"<!---toc start-->\n\n{table_of_contents}\n\n<!---toc end-->\n\n"
            f"{TOC_END_TAG}\n" + markdown
        )

    with open(outfile or path, "w") as fp:
        fp.write(new_markdown)

    click.echo(
        click.style(f"Success: wrote TOC to {outfile or path}", fg="green"), color=True
    )
