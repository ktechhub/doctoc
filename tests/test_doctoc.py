import pytest
from doctoc.markdown import toc, headers, get_links, as_link, escape
from doctoc.core import modify_and_write


@pytest.fixture
def sample_markdown():
    return """
    # Title 1
    
    ## Subtitle 1.1
    
    ### Sub-subtitle 1.1.1
    """


def test_modify_and_write(tmp_path):
    markdown_file = tmp_path / "test.md"
    markdown_file.write_text("# Title 1\n\n## Subtitle 1.1\n")

    modify_and_write(markdown_file)
    assert markdown_file.read_text().startswith(
        "<!-- START doctoc generated TOC please keep comment here to allow auto update -->"
    )


def test_get_links():
    md_string = "[Link](#header)"
    links = list(get_links(md_string))
    assert len(links) == 1
    assert links[0][0] == "Link"
    assert links[0][1] == "#header"


def test_as_link():
    assert as_link("Header with spaces") == "header-with-spaces"


if __name__ == "__main__":
    pytest.main()
