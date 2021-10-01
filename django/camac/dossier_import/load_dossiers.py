from typing import IO

import pyexcel


def prepare_cases(data):
    pass


def handle_case(case):
    store_case_attachments(case)


def store_case_attachments(case):
    pass


def perform_import(file: IO):
    # create an import case
    data = pyexcel.get_records(file)
    cases = prepare_cases(data)
    for case in cases:
        handle_case(case)
