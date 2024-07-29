#!/usr/bin/python3
import json
import os
import re
import subprocess
import sys
import tempfile

import tomli


def get_coverage_data():
    cov_json = tempfile.NamedTemporaryFile(suffix=".json")
    subprocess.check_call(
        # fail under 0 - we're not interested in whether full coverage is reached.
        [
            "coverage",
            "json",
            "--show-contexts",
            "-o",
            cov_json.name,
            "--fail-under=0",
            "--ignore-errors",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    cov_data = json.load(cov_json)
    return cov_data


def which_tests_for_code(file, line):
    cov_data = get_coverage_data()

    cov_info = cov_data["files"].get(file)
    if not cov_info:
        return []

    if line and line in cov_info["contexts"]:
        return cov_info["contexts"][line]
    else:
        all_contexts = sorted(
            set(
                [
                    ctx
                    for ctx_list in cov_info["contexts"].values()
                    for ctx in ctx_list
                    if ctx
                ]
            )
        )
        return all_contexts


def do_validate_test_locality(verbose, report_100percent):  # noqa: C901
    # We want each code to be tested by module-local or global test.
    # Accidental test coverage should be avoided
    cov_data = get_coverage_data()

    exempt_files = []

    try:
        with open("pyproject.toml", "rb") as fh_proj:
            pyproject = tomli.load(fh_proj)
            exempt_files = pyproject["tool"]["whichtest"]["exempt"]
    except Exception:
        # toml not readable or setting not present
        pass

    total_lines = 0
    total_foreign_covered = 0
    total_locally_covered = 0
    fully_covered = set()

    print("\nTest locality check report:\n")
    f_hdr = "File covered in test"
    print(f"{f_hdr:<62} Local   Other    %")
    print("-" * 88)

    for file, cov_info in cov_data["files"].items():
        if any(re.match(pattern, file) for pattern in exempt_files):
            # print(f"Skipping {file} - excluded by exempt rule")
            continue

        parts = file.split("/")
        if len(parts) > 2:
            acceptable_prefix = ".".join(parts[:2])
        if len(parts) == 2:
            # camac/foo.py - needs test in camac/ somewhere
            acceptable_prefix = parts[0] + ".tests"
        elif len(parts) == 1:
            # global (not even in the "camac" folder)
            acceptable_prefix = "tests"

        # print(f"{file}: acceptable test prefix: {acceptable_prefix}")
        # continue
        complaints = []

        for line, ctxes in cov_info["contexts"].items():
            if any(ctx.startswith(acceptable_prefix) for ctx in ctxes):
                # line covered by "one of our" tests - good
                continue

            if ctxes == [""]:
                # ctx of '' means covered by non-test. This implies
                # that it's probably module-scope code that was imported
                # outside the context of an actual test. We don't complain
                # about that stuff
                continue
            complaints.append(line)

        verbose_info = ""
        if complaints and verbose:
            offending_ranges = ", ".join(
                _compress_ranges(cov_info["contexts"].keys(), complaints)
            )
            verbose_info = f"(no cov in {acceptable_prefix}: {offending_ranges})"

        n_lines = len(cov_info["contexts"])
        n_complaints = len(complaints)
        n_local_covered = n_lines - n_complaints
        if n_lines:
            if len(file) > 60:
                file = f"...{file[-55:]}"

            coverage_percent = n_local_covered / n_lines * 100
            if coverage_percent == 100:
                fully_covered.add(file)
            if coverage_percent < 100 or report_100percent:
                print(
                    f"{file:<62} "
                    f"{n_local_covered:>4.0f}  {n_complaints:>4.0f}  "
                    f"{coverage_percent:>5.1f}%"
                    f" {verbose_info}"
                )
        total_lines += n_lines
        total_foreign_covered += n_complaints
        total_locally_covered += n_local_covered
    print("-" * 88)

    if not report_100percent:
        nfiles = len(fully_covered)
        print(f"\n{nfiles} files are fully tested locally and not shown\n")

    return total_locally_covered / total_lines


def _compress_ranges(all_nums, to_compress):
    all_nums = sorted([int(n) for n in all_nums])
    to_compress = sorted([int(n) for n in to_compress])

    # The [-1] ensures that when we reach the end in the *checking* loop,
    # there is the condition next_to_compress > next_valid, and therefore
    # allows us to treat every iteration the same
    next_valid = {num: succ for num, succ in zip(all_nums, all_nums[1:] + [-1])}

    if not all_nums:
        return []

    ranges = []
    start = to_compress[0]

    for num, nextnum in zip(to_compress, to_compress[1:] + [0]):
        # The [0] at the end conveniently also allows us to cover the last
        # iteration correctly
        next_valid_num = next_valid[num]

        if nextnum > next_valid_num or not nextnum:
            # range ends here - there's a gap
            ranges.append((start, num))
            start = nextnum

    text_ranges = [f"{n0}-{n1}" if n0 != n1 else str(n0) for n0, n1 in ranges]
    return text_ranges


def do_show_tests_for_code(filenames):
    for filename in filenames:
        file = filename
        line = None
        if ":" in file:
            file, line = file.split(":")

        ind = "    "
        tests = which_tests_for_code(file, line)

        lines = f"\n{ind}".join(tests)
        print(f"{filename} is covered by:\n{ind}{lines}")


HELP_TEXT = """
whichtest.py - inspect coverage data

This utility allows you to inspect coverage data to find out which test
is covering which part of your code. Useful to figure out which tests to run
locally when you changed a particular piece of code.

Note: This requires up-to-date coverage data, which can be obtained by running
`pytest --cov`. If you don't have current coverage data, you may get errors, or
invalid output

Usage:

* python whichtest.py path/to_some_file.py
* python whichtest.py path/to_some_file.py:123

This will give you a list of test cases for the given file, or, if you pass
the line number as well, just for the given line.


* python whichtest.py --check-locality
* python whichtest.py --check-locality [-v|--verbose] [--no-report-100percent]

Output the test locality score: The number of lines that are covered, across
the code base, by a test within the same module / django app.

If you enable verbose mode, it will output every line that's not covered by
a "local" test.

If the `--no-report-100percent` flag is given, then files that are 100% covered
locally are not reported.

Note that this is rather generic and certain cases are not caught correctly yet:
For example urls.py files may be re-imported by some tests, but also at django
startup, so they look like "foreign covered" in here despite being strictly
declarative/module-scope code only. This is a limitation of coverage.py.
""".strip()

MIN_LOCALITY_SCORE = int(os.environ.get("MIN_LOCALITY_SCORE", 90))

if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    report_100percent = "--no-report-100percent" not in sys.argv

    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
        print(HELP_TEXT)
    elif "--check-locality" in sys.argv:
        factor = do_validate_test_locality(verbose, report_100percent)
        percentage = factor * 100
        print(f"Test locality score: {percentage:.1f}%")
        if percentage < MIN_LOCALITY_SCORE:
            print(f"Minimum locality score below {MIN_LOCALITY_SCORE}!\n")
            print("Write more tests local to your code to avoid accidental-only")
            print("coverage! If a test in module A covers code in module B")
            print("we assume it's not explicitly testing B's feature and")
            print("therefore the feature is not actually tested.")
            sys.exit(1)

    else:
        non_flags = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
        do_show_tests_for_code(non_flags)
