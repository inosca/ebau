#!/usr/bin/env python3

"""parse, sort and format Django data dumps. """

import argparse
import json
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='parse, sort and format Django data dumps'
    )
    parser.add_argument('file', nargs=1, type=argparse.FileType('r+'),
                        help='dump file to format')
    parser.add_argument('-o', nargs=1, type=argparse.FileType('w'),
                        help='Filename for output', dest='output')
    parser.add_argument('-i', action='store_true',
                        help='Modify dump in-place (overwrite it)', dest='inPlace')

    args = parser.parse_args()

    data = json.load(args.file[0])
    data = sorted(data, key=lambda k: (k['model'], k['pk']))

    stdout = sys.stdout
    if args.output:
        stdout = args.output[0]
    if args.inPlace:
        stdout = args.file[0]
        stdout.seek(0)
        stdout.truncate()

    json.dump(data, stdout, indent=2, sort_keys=True)
    stdout.flush()
