#!/usr/bin/env python3

# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import re

from devscripts.utils import get_filename_args, read_file, write_file

VERBOSE = '''
  - type: checkboxes
    id: verbose
    attributes:
      label: Provide verbose output that clearly demonstrates the problem
      description: |
        This is mandatory unless absolutely impossible to provide. If you are unable to provide the output, please explain why.
      options:
        - label: Yes
          value: yes
          default: true
        - label: No
          value: no
      required: true
'''.strip()

NO_SKIP = '''
  - type: markdown
    attributes:
      value: |
        > [!IMPORTANT]
        > Not providing the required (*) information or removing the template will result in your issue being closed and ignored.
'''.strip()


def main():
    fields = {
        'no_skip': NO_SKIP,
        'verbose': VERBOSE,
        'verbose_optional': re.sub(r'(\n\s+validations:)?\n\s+required: true', '', VERBOSE),
    }

    infile, outfile = get_filename_args(has_infile=True)
    write_file(outfile, read_file(infile) % fields)


if __name__ == '__main__':
    main()
