#!/usr/bin/python3

import sys
from collections import defaultdict
import functools
import re
import yaml
import subprocess
import os
import jinja2

CONFIG_FILE = os.environ.get("TEST_ADVISOR_CONFIG", __file__.replace(".py", ".yaml"))

HELP_TEXT = f"""
Inosca Test Advisor

This utility is intended to track changes in the code and suggest areas
that may be affected by them.

Usage:

   {sys.argv[0]} from_rev [to_rev] > report.md
   {sys.argv[0]} --help

The `from_rev` and `to_rev` are git hash-like (tag or branch) to determine
the time range to check. If `to_rev` is left out, the current HEAD (latest
commit) is assumed.

The output is in Markdown format, structured as a checklist, so it can be
used for example in CodiMD to track completion of the manual tests.

Parameters:
    --help     Show this help text

Environment variables:

    $TEST_ADVISOR_CONFIG (default {CONFIG_FILE}): contains mapping of
                         code to modules as well as secondary affected
                         modules

""".strip()


class hdict(dict):
    def __hash__(self):
        return hash(tuple(sorted((k, v) for k, v in self.items())))


def show_help():
    print(HELP_TEXT)
    sys.exit(1)


def load_config():
    with open(CONFIG_FILE) as fh:
        return yaml.safe_load(fh)


def get_affected_files(from_rev, to_rev):
    out = subprocess.check_output(
        [
            "git",
            "log",
            "--name-only",
            "--pretty=format:COMMIT:%H",
            f"{from_rev}..{to_rev}",
        ]
    ).decode("utf-8")
    files_to_commits = defaultdict(list)
    current_commit = None
    for line in out.splitlines():
        if line.startswith("COMMIT:"):
            _, current_commit = line.strip().split(":")
        elif "/" in line:
            files_to_commits[line.strip()].append(current_commit)
        # else: Empty line, or something else. Ignoring

    return dict(files_to_commits)


def get_affected_modules(changed_files, config):
    result = defaultdict(
        lambda: {
            "commits": set(),
            "test_reason": set(),
            "also_affects": set(),
            "matched_files": set(),
            "affected_cantons": "",
        }
    )
    for file, relevant_commits in changed_files.items():
        for module in config["modules"]:
            module_name = module["name"]
            for pattern in module.get("files") or []:
                if re.match(pattern, file):
                    result[module_name]["affected_cantons"] = (
                        module.get("affected_cantons") or []
                    )
                    result[module_name]["test_reason"].add(
                        "Modified files (see commits below)"
                    )
                    result[module_name]["matched_files"].add(file)

                    for other_mod in module.get("affects_modules") or []:
                        result[other_mod]["test_reason"].add(
                            f"Possible side effects from module **{module_name}**"
                        )
                        result[module_name]["also_affects"].add(other_mod)

                    # REcord the commits that caused this module's change
                    result[module_name]["commits"].update(
                        [get_commit_info(c) for c in relevant_commits]
                    )
    return dict(result)


@functools.cache
def get_commit_info(commit):
    out = subprocess.check_output(["git", "cat-file", "commit", commit]).decode("utf-8")
    lines = out.splitlines()
    header_mode = True
    author = None
    for line in lines:
        line = line.strip()
        if header_mode and line.startswith("author "):
            parts = line.split()
            parts.pop()  # timezone
            parts.pop()  # timestamp
            parts.pop(0)  # "author" record info
            author = " ".join(parts)
        if header_mode and line == "":
            header_mode = False
        if line and not header_mode:
            message = line
            # we're only interested in the first line
            break

    return hdict({"commit": commit, "header": message, "author": author})


def main():
    if len(sys.argv) < 2 or "--help" in sys.argv:
        show_help()

    config = load_config()
    from_rev = sys.argv[1]
    to_rev = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

    affected_files = get_affected_files(from_rev, to_rev)

    affected_modules = get_affected_modules(affected_files, config)
    template = jinja2.Template(config["report_template"])
    context = {
        "from_rev": from_rev,
        "to_rev": to_rev,
        "affected_modules": affected_modules,
        "config": config,
    }
    print(template.render(context))


if __name__ == "__main__":
    main()
