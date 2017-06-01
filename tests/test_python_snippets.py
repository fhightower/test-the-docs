"""Test each of the code snippets in the python SDK docs."""
import os
import re
import subprocess
import sys

default_file = "./test.py"


def get_code_snippets(file_text):
    """Identify all of the code snippets in the documentation."""
    code_block_pattern = "(\.\. \n    no-test\n\n)?\.\. code-block:: python\n((.*\n)*?)[\S]"

    code_blocks = re.findall(code_block_pattern, file_text)

    # add the code (codeblock[1]) for each code block that is not prefixed with a "no-test" comment (codeblock[0])
    return [codeblock[1] for codeblock in code_blocks if codeblock[0] == ""]


def test_snippets():
    """Test all of the code snippets in the python SDK docs."""
    # keep a count of everything that happens when this file is run
    counter = {
        'expected_error': 0,
        'success': 0,
        'unexpected_error': 0,
    }

    # iterate through the .rst files in the ../docs/ directory
    for path, dirs, files in os.walk("../docs/"):
        # for each file in the current path
        for file_ in files:
            # if the file is a restructured text file
            if file_.endswith(".rst"):
                code_blocks = None

                # parse the code blocks from the file
                with open(os.path.join(path, file_), 'r') as f:
                    # get the code blocks
                    code_blocks = get_code_snippets(f.read())

                # test each of the code blocks
                for code_block in code_blocks:
                    # pattern for ":linenos:" and ":emphasize-lines:"
                    line_num_pattern = ":.*?line.*?:.*"

                    # remove any properties of the code snippet (:emphasize-lines: or :line-nos:)
                    code_block = re.sub(line_num_pattern, "", code_block)

                    # remove the indentation (this can be adjusted to remove as many tabs as you need)
                    code_block = re.sub("\n    ", "\n", code_block)

                    # write the python snippet to a file
                    with open(default_file, 'w+') as f:
                        f.write(code_block)

                    try:
                        # run test.py using python
                        subprocess.check_output(["python", "{}".format(default_file)])
                        counter['success'] += 1
                    except subprocess.CalledProcessError:
                        # if there is an exception, run it again and get the output
                        error_output = subprocess.getoutput("python {}".format(default_file))

                        # sometimes we expect an error to occur, so we can ignore those errors
                        if "Access Denied" in error_output:
                            counter['expected_error'] += 1
                        # if the output was UNEXPECTED, make a note of it
                        else:
                            print("\n\n{}:\n{}".format(os.path.join(path, file_), error_output))
                            counter['unexpected_error'] += 1

    # report the damage
    print("Successes: {}\nExpected Errors: {}\nUnexpected Errors: {}".format(counter['success'],
                                                                             counter['expected_error'],
                                                                             counter['unexpected_error']))

    # exit with a partial failure if there were unexpected errors
    if counter['unexpected_error'] > 0:
        sys.exit(3)
