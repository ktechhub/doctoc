import pytest
from click.testing import CliRunner
from doctoc.cli import main
from doctoc.markdown import as_link, escape, get_links, headers, toc
from doctoc.core import is_current, modify_and_write, TOC_START_TAG, TOC_END_TAG

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
    assert as_link("Section 1.2") == "section-1-2"


def test_as_link_leading_trailing_hashes():
    assert as_link("## My Header ##") == "my-header"


def test_as_link_numbered_heading():
    # GitHub converts periods between numbers to hyphens too, not just spaces.
    assert as_link("1.1 My first header") == "1-1-my-first-header"


def test_as_link_numbered_heading_no_double_hyphen():
    # A period immediately followed by a space must not produce a double hyphen.
    assert as_link("1. My first header") == "1-my-first-header"


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


def test_toc_exclude_no_match():
    md = "# H1\n## H2"
    result = toc(md, exclude=["Appendix"])
    assert "H1" in result
    assert "H2" in result


def test_toc_exclude_one_match():
    md = "# H1\n## Appendix\n## H2"
    result = toc(md, exclude=["Appendix"])
    assert "H1" in result
    assert "H2" in result
    assert "Appendix" not in result


def test_toc_exclude_multiple_values():
    md = "# H1\n## Appendix\n## Notes\n## H2"
    result = toc(md, exclude=["Appendix", "Notes"])
    assert "H1" in result
    assert "H2" in result
    assert "Appendix" not in result
    assert "Notes" not in result


def test_toc_exclude_preserves_nesting_of_remaining_headers():
    # Excluding the top-level header should not shift the indentation
    # baseline for the remaining (deeper) headers.
    md = "# Appendix\n## H1\n### H2"
    result = toc(md, exclude=["Appendix"])
    lines = result.split("\n")
    assert lines[0].startswith("* [H1]")
    assert lines[1].startswith("  * [H2]")


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


def test_modify_and_write_is_idempotent(tmp_path):
    # Re-running on a file that already has a current TOC must not change it
    # (previously each re-run inserted an extra blank line, growing the file
    # without bound).
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n\n## Subtitle 1.1\n")

    modify_and_write(md_file)
    once = md_file.read_text()
    modify_and_write(md_file)
    twice = md_file.read_text()

    assert once == twice


# ---------------------------------------------------------------------------
# is_current() / --check
# ---------------------------------------------------------------------------


def test_is_current_false_when_no_toc_yet(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n\n## Subtitle 1.1\n")

    assert is_current(md_file) is False


def test_is_current_true_after_write(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n\n## Subtitle 1.1\n")

    modify_and_write(md_file)
    assert is_current(md_file) is True


def test_is_current_false_when_toc_stale(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n\n## Subtitle 1.1\n")

    modify_and_write(md_file)
    with md_file.open("a") as fp:
        fp.write("\n## New Section\n")

    assert is_current(md_file) is False


def test_is_current_does_not_write(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n")

    is_current(md_file)
    assert md_file.read_text() == "# Title 1\n"


def test_cli_check_exits_zero_when_current(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n")
    modify_and_write(md_file)

    result = CliRunner().invoke(main, ["--check", str(md_file)])
    assert result.exit_code == 0
    assert "OK" in result.output


def test_cli_check_exits_nonzero_when_stale(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title 1\n")

    result = CliRunner().invoke(main, ["--check", str(md_file)])
    assert result.exit_code != 0
    assert "STALE" in result.output
    assert str(md_file) in result.output


def test_cli_check_does_not_write(tmp_path):
    md_file = tmp_path / "test.md"
    original = "# Title 1\n"
    md_file.write_text(original)

    CliRunner().invoke(main, ["--check", str(md_file)])
    assert md_file.read_text() == original


def test_cli_exclude_option(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title\n## Appendix\n## Notes\n")

    result = CliRunner().invoke(main, ["--exclude", "Appendix", str(md_file)])
    assert result.exit_code == 0
    toc_section = md_file.read_text().split(TOC_END_TAG)[0]
    assert "Notes" in toc_section
    assert "Appendix" not in toc_section


def test_cli_exclude_option_multiple_values(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title\n## Appendix\n## Notes\n## Keep\n")

    result = CliRunner().invoke(
        main, ["--exclude", "Appendix", "--exclude", "Notes", str(md_file)]
    )
    assert result.exit_code == 0
    toc_section = md_file.read_text().split(TOC_END_TAG)[0]
    assert "Keep" in toc_section
    assert "Appendix" not in toc_section
    assert "Notes" not in toc_section


def test_cli_check_reports_multiple_files(tmp_path):
    stale_file = tmp_path / "stale.md"
    stale_file.write_text("# Title 1\n")
    current_file = tmp_path / "current.md"
    current_file.write_text("# Title 2\n")
    modify_and_write(current_file)

    result = CliRunner().invoke(main, ["--check", str(stale_file), str(current_file)])
    assert result.exit_code != 0
    assert f"STALE: {stale_file}" in result.output
    assert f"OK: {current_file}" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
