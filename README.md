<!-- START doctoc generated TOC please keep comment here to allow auto update -->

**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*

<!---toc start-->

- [DocToc](#doctoc)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Options:](#options)
  - [Features](#features)
  - [GitHub](#github)
  - [License](#license)
    - [Contribution](#contribution)

<!---toc end-->

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# DocToc

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg)
[![PyPI version](https://badge.fury.io/py/doctoc.svg)](https://badge.fury.io/py/doctoc)

DocToc is a command-line tool built with Python that automatically generates and updates table of contents (TOC) for Markdown files. It scans through your Markdown file, identifies headers, and creates a TOC with clickable links.

## Prerequisites
Before installing DocToc, ensure you have the following:
- Python 3.6+
- pip (Python package installer)

## Installation
You can install DocToc using pip:

```sh
pip install doctoc
```
Alternatively, you can install it from the source on GitHub:

```sh
git clone https://github.com/ktechhub/doctoc.git
cd doctoc
python setup.py install
```

## Usage
Generate a table of contents for a Markdown file:

```sh
doctoc --help
Usage: doctoc [OPTIONS] MARKDOWN_FILE

  Generate or update a table of contents for Markdown files and optionally
  check hyperlinks.

  Args:
  markdown_file (str): Path to the Markdown file to process.
  outfile (str, optional): Output file path. If specified, writes the modified content to this file instead of overwriting the original.
  check_links (bool): Flag to enable checking the validity of hyperlinks found in the Markdown file.

Options:
  -o, --outfile TEXT  Specify an output file instead of overwriting.
  -cl, --check-links  Check validity of hyperlinks.
  --help              Show this message and exit.
```

### Options:

- `--outfile`: Specify an output file instead of overwriting.
- `--check-links`: Check the validity of hyperlinks within the Markdown file.

Example with options:
```sh
doctoc README.md --check-links
```
Output
```sh
Success: wrote TOC to README.md
Checking hyperlinks...
VALID: [DocToc](https://github.com/ktechhub/doctoc)
VALID: [DocToc](#doctoc)
VALID: [Prerequisites](#prerequisites)
VALID: [Installation](#installation)
VALID: [Usage](#usage)
VALID: [Options:](#options)
VALID: [Features](#features)
VALID: [GitHub](#github)
VALID: [License](#license)
VALID: [GitHub repository](https://github.com/ktechhub/doctoc)
```

```sh
doctoc README.md --outfile README_with_toc.md
```
Output
```sh
Success: wrote TOC to README_with_toc.md
```
```sh
doctoc README.md --outfile README_with_toc.md --check-links
```

## Features
- Automatically generates a TOC based on Markdown headers.
- Supports customization with options to specify output file and check link validity.
- Simple and easy to use with a command-line interface.

## GitHub
For more details, visit the [GitHub repository](https://github.com/ktechhub/doctoc).

## License
This project is licensed under the MIT License - see the LICENSE file for details.

### Contribution
If you want to contribute, kindly see this **[contribution](https://github.com/ktechhub/doctoc/tree/main/contribution.md)**