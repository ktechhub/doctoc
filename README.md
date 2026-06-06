<!-- START doctoc generated TOC please keep comment here to allow auto update -->

**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*

<!---toc start-->

* [DocToc](#doctoc)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Options](#options)
  * [Examples](#examples)
  * [Features](#features)
  * [GitHub](#github)
  * [License](#license)
  * [Contribution](#contribution)

<!---toc end-->

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# DocToc

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg)
[![PyPI version](https://badge.fury.io/py/doctoc.svg)](https://badge.fury.io/py/doctoc)

DocToc is a command-line tool that automatically generates and updates a table of contents (TOC) for Markdown files. It scans your Markdown, identifies headers, and inserts a TOC with clickable links — skipping headers inside fenced code blocks.

## Prerequisites

- Python 3.8+
- pip

## Installation

```sh
pip install doctoc
```

Or from source:

```sh
git clone https://github.com/ktechhub/doctoc.git
cd doctoc
pip install .
```

## Usage

```sh
doctoc [OPTIONS] MARKDOWN_FILES...
```

`MARKDOWN_FILES` accepts one or more file paths or glob patterns:

```sh
doctoc README.md
doctoc docs/README.md CHANGELOG.md
doctoc '**/*.md'
```

On the first run, DocToc inserts the TOC at the top of the file. On subsequent runs it updates the existing TOC in place.

## Options

| Option | Short | Description |
|---|---|---|
| `--outfile PATH` | `-o` | Write output to a separate file instead of overwriting the input (single-file only). |
| `--check-links` | `-cl` | Validate all hyperlinks found in the file. |
| `--title TEXT` | `-t` | Custom title line for the TOC block (default: bold "Table of Contents" with attribution). |
| `--max-depth INT` | `-d` | Limit TOC to headings up to this depth (e.g. `2` includes only H1 and H2). |
| `--help` | | Show help and exit. |

## Examples

**Basic — generate or update TOC:**
```sh
doctoc README.md
# Success: wrote TOC to README.md
```

**Custom output file:**
```sh
doctoc README.md -o README_with_toc.md
# Success: wrote TOC to README_with_toc.md
```

**Limit TOC depth to H1 and H2 only:**
```sh
doctoc README.md --max-depth 2
```

**Custom TOC title:**
```sh
doctoc README.md --title "## Contents"
```

**Check hyperlinks after generating TOC:**
```sh
doctoc README.md --check-links
# Success: wrote TOC to README.md
# Checking hyperlinks in README.md...
# VALID: [DocToc](#doctoc)
# VALID: [Installation](#installation)
# VALID: [GitHub repository](https://github.com/ktechhub/doctoc)
# INVALID: [Broken](#missing-section)
```

**Process all Markdown files recursively:**
```sh
doctoc '**/*.md'
```

## Features

- Generates and updates a TOC based on Markdown headers.
- Skips headers inside fenced code blocks (` ``` ` and `~~~`).
- Supports multiple files and glob patterns in a single invocation.
- `--max-depth` to limit which heading levels appear in the TOC.
- `--title` to customise the TOC heading line.
- Link checker validates both internal anchor links and external HTTP(S) URLs, with a timeout and clear error output.
- Writes to an optional output file instead of overwriting the source.

## GitHub

For more details, visit the [GitHub repository](https://github.com/ktechhub/doctoc).

## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Contribution

If you want to contribute, kindly see **[contribution](https://github.com/ktechhub/doctoc/tree/main/contribution.md)**.
