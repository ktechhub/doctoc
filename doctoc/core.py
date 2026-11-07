import difflib
import re

from .markdown import HEADER_PAT, toc

TOC_START_TAG = (
    "<!-- START doctoc generated TOC please keep comment here to allow auto update -->"
)
TOC_END_TAG = (
    "<!-- END doctoc generated TOC please keep comment here to allow auto update -->"
)

_TOC_HEADER_TEMPLATE = "**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*"

# Matches a heading whose text is just "Table of Contents", "Contents", or
# "TOC" (optionally followed by a colon) -- the common hand-written variants.
_EXISTING_TOC_HEADING_PAT = re.compile(
    r"^[ \t]{0,3}#{1,6}[ \t]+(table of contents|contents|toc)[ \t:]*$",
    re.IGNORECASE | re.MULTILINE,
)

# A Markdown list item line that itself contains a link, e.g. "* [H1](#h1)".
_LIST_LINK_LINE_PAT = re.compile(r"^[ \t]*[-*+][ \t]+.*\[[^\]]+\]\([^)]+\)")


class ExistingUnmanagedTocError(Exception):
    """Raised when a file has a hand-written, un-tagged TOC-like section."""


def _find_existing_toc_section(markdown):
    """Detect a hand-written "Table of Contents"-style section that has no
    doctoc markers around it.

    Returns (start, end) spanning from the heading line through the end of
    the list of links beneath it, or None if nothing matches. A heading
    that merely happens to be titled "Table of Contents" but isn't actually
    followed by a list of links (e.g. prose) is deliberately *not* treated
    as a match, to avoid false positives.
    """
    for heading_match in _EXISTING_TOC_HEADING_PAT.finditer(markdown):
        start = heading_match.start()
        pos = heading_match.end()
        if pos < len(markdown) and markdown[pos] == "\n":
            pos += 1

        end = pos
        saw_list_link = False
        for line in markdown[pos:].split("\n"):
            if line.strip() == "":
                end += len(line) + 1
                continue
            if HEADER_PAT.match(line) or not _LIST_LINK_LINE_PAT.match(line):
                break
            saw_list_link = True
            end += len(line) + 1

        if saw_list_link:
            return start, end
    return None


def _toc_block(table_of_contents, title):
    header_line = title or _TOC_HEADER_TEMPLATE
    return (
        TOC_START_TAG
        + "\n\n"
        + f"{header_line}\n\n"
        + f"<!---toc start-->\n\n{table_of_contents}\n\n<!---toc end-->\n\n"
        + TOC_END_TAG
    )


def _insert_index(markdown, after):
    """Return the offset to insert a fresh TOC block at.

    Defaults to the top of the file (0). If `after` is given, inserts right
    after the first line containing it; falls back to the top if no line
    matches.
    """
    if after is None:
        return 0

    match = re.search(
        r"^.*" + re.escape(after) + r".*\n?", markdown, flags=re.MULTILINE
    )
    return match.end() if match else 0


def _render(
    markdown, title=None, max_depth=None, exclude=None, after=None, wrap_existing=False
):
    table_of_contents = toc(markdown, max_depth=max_depth, exclude=exclude)
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

    existing = _find_existing_toc_section(markdown)
    if existing is not None:
        existing_start, existing_end = existing
        if not wrap_existing:
            raise ExistingUnmanagedTocError(
                "Found an existing, hand-written 'Table of Contents'-style "
                "section with no doctoc markers. Re-run with --wrap-existing "
                "to let doctoc manage it going forward, or remove it "
                "manually first."
            )
        wrapped = (
            TOC_START_TAG
            + "\n\n"
            + markdown[existing_start:existing_end].rstrip("\n")
            + "\n\n"
            + TOC_END_TAG
            + "\n"
        )
        return markdown[:existing_start] + wrapped + markdown[existing_end:]

    insert_at = _insert_index(markdown, after)
    new_block = (
        toc_section
        + "\n"
        + f"<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n"
    )
    return markdown[:insert_at] + new_block + markdown[insert_at:]


def modify_and_write(
    path,
    outfile=None,
    title=None,
    max_depth=None,
    exclude=None,
    backup=False,
    after=None,
    wrap_existing=False,
):
    with open(path) as fp:
        markdown = fp.read()

    if backup:
        with open(f"{path}.bak", "w") as fp:
            fp.write(markdown)

    new_markdown = _render(
        markdown,
        title=title,
        max_depth=max_depth,
        exclude=exclude,
        after=after,
        wrap_existing=wrap_existing,
    )

    dest = outfile or path
    with open(dest, "w") as fp:
        fp.write(new_markdown)

    return dest


def render_diff(
    path, title=None, max_depth=None, exclude=None, after=None, wrap_existing=False
):
    """Return a unified diff of what modify_and_write would change, without writing.

    Returns an empty string if path's TOC is already current.
    """
    with open(path) as fp:
        markdown = fp.read()

    new_markdown = _render(
        markdown,
        title=title,
        max_depth=max_depth,
        exclude=exclude,
        after=after,
        wrap_existing=wrap_existing,
    )
    if new_markdown == markdown:
        return ""

    path_str = str(path)
    return "".join(
        difflib.unified_diff(
            markdown.splitlines(keepends=True),
            new_markdown.splitlines(keepends=True),
            fromfile=path_str,
            tofile=path_str,
        )
    )


def is_current(
    path, title=None, max_depth=None, exclude=None, after=None, wrap_existing=False
):
    """Return True if path's TOC already matches what doctoc would generate.

    Never writes to disk.
    """
    with open(path) as fp:
        markdown = fp.read()

    return markdown == _render(
        markdown,
        title=title,
        max_depth=max_depth,
        exclude=exclude,
        after=after,
        wrap_existing=wrap_existing,
    )
