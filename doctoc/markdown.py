import re
import collections

TOC_PAT = re.compile(r"[ \t]*<!---toc start-->(.*?)<!---toc end-->\s*", flags=re.DOTALL)

MD_LINK_PAT = re.compile(r"\[([^\[\]]+)\]\((([^\s)(]|\([^\s)(]*\))*)\)", re.M)

HEADER_PAT = re.compile(r"^\s{,3}(#{1,6})\s+(.*)")

STRIP_CANDIDATE_PAT = re.compile(r"(?<!\\)[ \t#]+$|^[ \t#]+")

ITAL_PAT = re.compile(r"(?<!\\)_[^(?<!\\)_]+(?<!\\)_")
BOLD_PAT = re.compile(r"(?<!\\)\*[^(?<!\\)\*]+(?<!\\)\*")

FENCE_PAT = re.compile(r"^[ \t]*(```|~~~)")


class MarkdownError(Exception):
    """Markdown formatted incorrectly & unparseable."""


def _strip(x):
    return STRIP_CANDIDATE_PAT.sub("", x)


def _replace_ital_bold(s):
    to_repl = "_*"
    for pat in (ITAL_PAT, BOLD_PAT):
        for match in pat.finditer(s):
            found = match.group(0)
            s = s.replace(found, found.strip(to_repl))
    return s


def as_link(x):
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
    return x.replace("[", "\\[").replace("]", "\\]")


def get_links(md_string):
    lines = md_string.split("\n")
    line_number = 0
    for line in lines:
        line_number += 1
        for match in re.finditer(MD_LINK_PAT, line):
            link_text = match.group(1)
            link_url = match.group(2)
            col_start = match.start(2)
            yield link_text, link_url, line_number, col_start


def toc(md_string, max_depth=None):
    entries = []
    n_seen = collections.defaultdict(int)
    min_level = None

    for level, header in headers(md_string):
        if max_depth is not None and level > max_depth:
            continue
        if min_level is None:
            min_level = level

        link = as_link(header)
        n = n_seen[link]
        if n > 0:
            n_seen[link] += 1
            link += "-" + str(n)
        else:
            n_seen[link] += 1

        indent = max(0, level - min_level)
        entries.append(
            "{spaces}* [{header}](#{link})".format(
                spaces="  " * indent,
                header=escape(_strip(header)),
                link=link,
            )
        )
    return "\n".join(entries)


def headers(md_string):
    in_fence = False
    fence_marker = None

    for line in md_string.split("\n"):
        fence_match = FENCE_PAT.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            continue

        if in_fence:
            continue

        header = HEADER_PAT.match(line)
        if header:
            level = len(header.group(1))
            yield level, header.group(2)
