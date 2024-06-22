import re
import collections

TOC_PAT = re.compile(r"[ \t]*<!---toc start-->(.*?)<!---toc end-->\s*", flags=re.DOTALL)

MD_LINK_PAT = re.compile(r"\[([^\[\]]+)\]\((([^\s)(]|\([^\s)(]*\))*)\)", re.M)

HEADER_PAT = re.compile(r"^\s{,3}(#{1,6})\s+(.*)")

STRIP_CANDIDATE_PAT = re.compile(r"(?<!\\)[ \t#]+$|^[ \t#]+")

ITAL_PAT = re.compile(r"(?<!\\)_[^(?<!\\)_]+(?<!\\)_")
BOLD_PAT = re.compile(r"(?<!\\)\*[^(?<!\\)\*]+(?<!\\)\*")


class MarkdownError(Exception):
    """Markdown formatted incorrectly & unparseable."""


def _strip(x):
    """
    Strip surrounding spaces, tabs, and hash signs from the input string `x`.

    This function removes leading and trailing whitespace characters (spaces and tabs),
    as well as leading hash signs (`#`) from the input string `x`.

    Args:
        x (str): The input string from which surrounding spaces, tabs, and hash signs should be stripped.

    Returns:
        str: A modified version of the input string `x` with leading and trailing spaces, tabs,
        and hash signs removed.

    Example:
        >>> _strip("  #  Hello, world!  #  ")
        "Hello, world!"

    Note:
        This function assumes the existence of `STRIP_CANDIDATE_PAT`, which is a regular expression
        pattern matching spaces, tabs, and hash signs. Ensure this pattern is defined and imported
        in the context where this function is used.

    """
    return STRIP_CANDIDATE_PAT.sub("", x)


def _replace_ital_bold(s):
    """
    Replace italic and bold formatting markers in the input string `s`.

    This function iterates through occurrences of italic and bold patterns (represented by
    `ITAL_PAT` and `BOLD_PAT` respectively) within the string `s`. It removes leading and trailing
    underscore (`_`) and asterisk (`*`) characters from these patterns. This is useful when
    processing Markdown text that includes inline formatting for italics and bold.

    Args:
        s (str): The input string where italic and bold markers need to be processed.

    Returns:
        str: A modified version of the input string `s` where italic and bold formatting markers
        have been adjusted to remove leading and trailing underscore (`_`) and asterisk (`*`)
        characters.

    Example:
        >>> _replace_ital_bold("_*italic and bold*_ text")
        "italic and bold text"

    Note:
        This function assumes the existence of `ITAL_PAT` and `BOLD_PAT` patterns that match the
        respective italic and bold formatting markers. Ensure these patterns are defined and
        imported in the context where this function is used.
    """
    to_repl = "_*"
    for pat in (ITAL_PAT, BOLD_PAT):
        for match in pat.finditer(s):
            found = match.group(0)
            s = s.replace(found, found.strip(to_repl))
    return s


def as_link(x):
    """
    Convert a Markdown header string into a valid relative URL.

    This function takes a Markdown header string, converts it to lowercase, removes special characters
    except hyphens and underscores, replaces spaces with hyphens, and handles italics and bolds. It ensures
    that resulting URLs are formatted correctly, particularly handling cases where the resulting string
    ends with double hyphens by stripping one hyphen.

    Args:
        x (str): The input Markdown header string to convert into a URL.

    Returns:
        str: A valid relative URL converted from the input Markdown header string.

    Example:
        >>> as_link("Introduction to Markdown Syntax")
        "introduction-to-markdown-syntax"

    Note:
        This function relies on the `_strip` and `_replace_ital_bold` helper functions to clean and format
        the input string `x`. Ensure these functions are correctly defined and imported in the context
        where this function is used.

    """
    res = re.sub(
        r"[^-\w\s]",
        "",
        re.sub(r"\s+", "-", _strip(x.lower())),
        flags=re.U,
    )
    res = _replace_ital_bold(res)

    if res.endswith("--"):
        res = res.strip("-") + "-"
    return res


def escape(x):
    """
    Escape square brackets '[' and ']'.

    This function takes a string `x` and escapes square brackets '[' and ']' by replacing them with
    their escaped counterparts '\\[' and '\\]'.

    Args:
        x (str): The input string containing square brackets '[' and/or ']'.

    Returns:
        str: The input string `x` with square brackets '[' and ']' escaped as '\\[' and '\\]'.

    Example:
        >>> escape("Example [String]")
        "Example \\[String\\]"
    """
    return x.replace("[", "\\[").replace("]", "\\]")


def get_links(md_string):
    """
    Find links in a Markdown string.

    This function searches through a given Markdown string `md_string` for Markdown-style links
    and yields tuples containing the link text, URL, line number, and column start index.

    Args:
        md_string (str): The Markdown string to search for links.

    Yields:
        tuple: A tuple containing four elements:
            - link_text (str): The text of the Markdown link.
            - link_url (str): The URL or target of the Markdown link.
            - line_number (int): The line number in the Markdown string where the link was found (1-indexed).
            - col_start (int): The column index in the line where the URL starts (0-indexed).
    Example:
        >>> md_string = "Here is a [sample link](https://example.com) in Markdown."
        >>> list(get_links(md_string))
        [('sample link', 'https://example.com', 1, 8)]

    Notes:
        - Assumes the Markdown links follow the format `[link_text](link_url)`.
    """
    lines = md_string.split("\n")
    line_number = 0
    for line in lines:
        line_number += 1
        for match in re.finditer(MD_LINK_PAT, line):
            link_text = match.group(1)
            link_url = match.group(2)
            col_start = match.start(2)
            yield link_text, link_url, line_number, col_start


def toc(md_string):
    """
    Generate a table of contents for a Markdown string.

    This function generates a table of contents (TOC) based on the headers found in the Markdown
    string `md_string`. It iterates through the headers, converts each header to a link, and
    formats it in Markdown syntax suitable for a TOC.

    Args:
        md_string (str): The Markdown string for which the TOC is to be generated.

    Returns:
        str: A Markdown-formatted string representing the table of contents.

    Example:
        >>> md_string = "# Header 1\n## Subheader 1.1\n### Subsubheader\n# Header 2"
        >>> print(toc(md_string))
        * [Header 1](#header-1)
          * [Subheader 1.1](#subheader-11)
            * [Subsubheader](#subsubheader)
        * [Header 2](#header-2)

    Notes:
        - Assumes headers are marked with Markdown syntax (#, ##, ###, etc.).
        - Uses `as_link`, `escape`, and `_strip` functions for link conversion and formatting.
    """
    toc = []
    n_seen = collections.defaultdict(int)

    for level, header in headers(md_string):
        link = as_link(header)
        n = n_seen[link]
        if n > 0:
            n_seen[link] += 1
            link += "-" + str(n)
        else:
            n_seen[link] += 1

        toc.append(
            "{spaces}* [{header}](#{link})".format(
                spaces="  " * (level - 1),
                header=escape(_strip(header)),
                link=link,
            )
        )
    return "\n".join(toc)


def headers(md_string):
    """
    Generate Markdown headers from a given Markdown string.

    This function iterates through each line of the Markdown string `md_string`,
    matches lines that start with Markdown header patterns defined in `HEADER_PAT`,
    and yields tuples of header levels and header titles.

    Args:
        md_string (str): The Markdown string to extract headers from.

    Yields:
        tuple: A tuple containing the header level (int) and header title (str).

    Example:
        >>> md_string = "# Header 1\n## Subheader 1.1\n### Subsubheader\n# Header 2"
        >>> list(headers(md_string))
        [(1, 'Header 1'), (2, 'Subheader 1.1'), (3, 'Subsubheader'), (1, 'Header 2')]

    Notes:
        - Assumes headers are marked with Markdown syntax (#, ##, ###, etc.).
        - Uses `HEADER_PAT` pattern for matching Markdown headers.
    """
    for line in md_string.split("\n"):
        header = HEADER_PAT.match(line)
        if header:
            level = len(header.group(1))
            header = header.group(2)
            yield level, header
