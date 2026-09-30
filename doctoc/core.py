from .markdown import toc

TOC_START_TAG = (
    "<!-- START doctoc generated TOC please keep comment here to allow auto update -->"
)
TOC_END_TAG = (
    "<!-- END doctoc generated TOC please keep comment here to allow auto update -->"
)

_TOC_HEADER_TEMPLATE = "**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*"


def _toc_block(table_of_contents, title):
    header_line = title or _TOC_HEADER_TEMPLATE
    return (
        TOC_START_TAG
        + "\n\n"
        + f"{header_line}\n\n"
        + f"<!---toc start-->\n\n{table_of_contents}\n\n<!---toc end-->\n\n"
        + TOC_END_TAG
    )


def _render(markdown, title=None, max_depth=None):
    table_of_contents = toc(markdown, max_depth=max_depth)
    toc_section = _toc_block(table_of_contents, title)

    start_index = markdown.find(TOC_START_TAG)
    end_index = markdown.find(TOC_END_TAG)

    if start_index != -1 and end_index != -1:
        end_index += len(TOC_END_TAG)
        # markdown[end_index:] already carries whatever separator followed the
        # previous END_TAG (e.g. the "\n<!-- DON'T EDIT... -->\n" boilerplate),
        # so no extra newline is added here — doing so would insert another
        # blank line on every re-run and make the output grow without bound.
        return markdown[:start_index] + toc_section + markdown[end_index:]
    else:
        return (
            toc_section
            + "\n"
            + f"<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n"
            + markdown
        )


def modify_and_write(path, outfile=None, title=None, max_depth=None):
    with open(path) as fp:
        markdown = fp.read()

    new_markdown = _render(markdown, title=title, max_depth=max_depth)

    dest = outfile or path
    with open(dest, "w") as fp:
        fp.write(new_markdown)

    return dest


def is_current(path, title=None, max_depth=None):
    """Return True if path's TOC already matches what doctoc would generate.

    Never writes to disk.
    """
    with open(path) as fp:
        markdown = fp.read()

    return markdown == _render(markdown, title=title, max_depth=max_depth)
