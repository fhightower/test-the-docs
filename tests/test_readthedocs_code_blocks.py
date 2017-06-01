"""Ensure the number of code-blocks shown on the live page matches the number of code-blocks in the rst files."""
import os
import re

import bs4
import requests

mappings = {
    '../docs/': 'https://test-the-docs.readthedocs.io/en/latest'
}


def get_code_blocks_from_rtd(readthedocs_link):
    """Count the code blocks on the read the docs page."""
    r = requests.get(readthedocs_link)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    code_divs = soup.findAll("div", {"class": "highlight"})
    return len(code_divs)


def get_code_blocks_from_rst(directory):
    """Find all of the code blocks in the restructured text files."""
    code_block_count = 0
    pattern = "\.\. code(-block)?::"

    for path, dirs, files in os.walk(directory):
        for file_ in files:
            with open(os.path.join(path, file_), 'r') as f:
                code_block_count += len(re.findall(pattern, f.read()))

    return code_block_count


def test_readthedocs_code_blocks():
    """Make sure the number of code-blocks on rtd is the number we are expecting from the rst files."""
    for mapping in mappings:
        readthedocs_code_blocks = get_code_blocks_from_rtd(mappings[mapping])
        rst_code_blocks = get_code_blocks_from_rst(mapping)

        print("\n{}".format(mapping.split("/")[-1].title().upper()))

        print("Code blocks in ReadTheDocs: {}".format(readthedocs_code_blocks))
        print("Code blocks in the RST files: {}".format(rst_code_blocks))

        assert readthedocs_code_blocks == rst_code_blocks
