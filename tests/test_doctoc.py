import pytest
from doctoc.markdown import as_link, escape, get_links, headers, toc
from doctoc.core import modify_and_write, TOC_START_TAG, TOC_END_TAG


# ---------------------------------------------------------------------------
# headers()
# ---------------------------------------------------------------------------

def test_headers_basic():
    md = "# H1\n## H2\n### H3"
    assert list(headers(md)) == [(1, "H1"), (2, "H2"), (3, "H3")]


def test_headers_skips_fenced_backtick():
    md = "# Real\n```\n# Fake\n```\n## Also Real"
    assert list(headers(md)) == [(1, "Real"), (2, "Also Real")]


def test_headers_skips_fenced_tilde():
    md = "# Real\n~~~\n# Fake\n~~~\n## Also Real"
    assert list(headers(md)) == [(1, "Real"), (2, "Also Real")]


def test_headers_fence_requires_matching_marker():
    # A backtick fence is NOT closed by a tilde fence
    md = "```\n# Fake\n~~~\n# Still Fake\n```\n# Real"
    assert list(headers(md)) == [(1, "Real")]


def test_headers_ignores_indented_code_block():
    # Indented-only (non-fenced) lines that look like headers are still parsed
    # because the HEADER_PAT allows up to 3 spaces of indent
    md = "# H1\n    # not a header (4 spaces)"
    result = list(headers(md))
    assert (1, "H1") in result
    assert not any(h == "not a header (4 spaces)" for _, h in result)


# ---------------------------------------------------------------------------
# as_link()
# ---------------------------------------------------------------------------

def test_as_link_basic():
    assert as_link("Header with spaces") == "header-with-spaces"


def test_as_link_special_chars():
    assert as_link("Hello, World!") == "hello-world"


def test_as_link_numbers():
    assert as_link("Section 1.2") == "section-12"


def test_as_link_leading_trailing_hashes():
    assert as_link("## My Header ##") == "my-header"


# ---------------------------------------------------------------------------
# escape()
# ---------------------------------------------------------------------------

def test_escape_brackets():
    assert escape("Example [String]") == "Example \\[String\\]"


def test_escape_no_brackets():
    assert escape("No brackets here") == "No brackets here"


# ---------------------------------------------------------------------------
# get_links()
# ---------------------------------------------------------------------------

def test_get_links_basic():
    md = "[Link](#header)"
    links = list(get_links(md))
    assert len(links) == 1
    assert links[0][0] == "Link"
    assert links[0][1] == "#header"


def test_get_links_multiple():
    md = "[A](#a) and [B](https://example.com)"
    links = list(get_links(md))
    assert len(links) == 2
    assert links[0][1] == "#a"
    assert links[1][1] == "https://example.com"


def test_get_links_line_numbers():
    md = "line1\n[Link](#h)\nline3"
    links = list(get_links(md))
    assert links[0][2] == 2


# ---------------------------------------------------------------------------
# toc()
# ---------------------------------------------------------------------------

def test_toc_basic():
    md = "# H1\n## H2\n### H3"
    result = toc(md)
    assert "* [H1](#h1)" in result
    assert "  * [H2](#h2)" in result
    assert "    * [H3](#h3)" in result


def test_toc_duplicate_headers():
    md = "# Intro\n# Intro\n# Intro"
    result = toc(md)
    assert "* [Intro](#intro)" in result
    assert "* [Intro](#intro-1)" in result
    assert "* [Intro](#intro-2)" in result


def test_toc_max_depth():
    md = "# H1\n## H2\n### H3\n#### H4"
    result = toc(md, max_depth=2)
    assert "H1" in result
    assert "H2" in result
    assert "H3" not in result
    assert "H4" not in result


def test_toc_max_depth_single_level():
    md = "# A\n## B\n# C"
    result = toc(md, max_depth=1)
    assert "A" in result
    assert "C" in result
    assert "B" not in result


def test_toc_indentation_starts_at_first_level():
    # When document starts at H2, indentation should be relative (no leading spaces)
    md = "## First\n### Second"
    result = toc(md)
    lines = result.split("\n")
    assert lines[0].startswith("* ")
    assert lines[1].startswith("  * ")


def test_toc_skips_code_fence_headers():
    md = "# Real\n```\n# Fake\n```\n## Also Real"
    result = toc(md)
    assert "Real" in result
    assert "Also Real" in result
    assert "Fake" not in result


def test_toc_special_chars_in_header():
    md = "# Hello [World]"
    result = toc(md)
    assert "\\[World\\]" in result


# ---------------------------------------------------------------------------
# modify_and_write()
# ---------------------------------------------------------------------------

def test_modify_and_write_inserts_toc(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n\n## Subtitle 1.1\n")

    modify_and_write(md_file)
    content = md_file.read_text()
    assert content.startswith(TOC_START_TAG)
    assert TOC_END_TAG in content
    assert "Title 1" in content


def test_modify_and_write_updates_existing_toc(tmp_path):
    md_file = tmp_path / "test.md"
    initial = (
        f"{TOC_START_TAG}\n\n"
        "**Table of Contents**\n\n"
        "<!---toc start-->\n\n* [Old](#old)\n\n<!---toc end-->\n\n"
        f"{TOC_END_TAG}\n"
        "# New Header\n"
    )
    md_file.write_text(initial)

    modify_and_write(md_file)
    content = md_file.read_text()
    assert "New Header" in content
    assert "Old" not in content


def test_modify_and_write_outfile(tmp_path):
    src = tmp_path / "src.md"
    dest = tmp_path / "out.md"
    src.write_text("# Title\n")

    modify_and_write(src, outfile=str(dest))
    assert dest.exists()
    assert not src.read_text().startswith(TOC_START_TAG)
    assert dest.read_text().startswith(TOC_START_TAG)


def test_modify_and_write_custom_title(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title\n")

    modify_and_write(md_file, title="My Custom Title")
    assert "My Custom Title" in md_file.read_text()


def test_modify_and_write_max_depth(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# H1\n## H2\n### H3\n")

    modify_and_write(md_file, max_depth=2)
    content = md_file.read_text()
    assert "H1" in content
    assert "H2" in content
    assert "H3" not in content.split(TOC_END_TAG)[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
