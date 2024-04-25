# CAMAC Tools collection

This directory is intended for various tools that support development.

## Diffdumps

A tool to resolve conflicts in django "dumpdata" files.

This is best used in a three-way merge situation, which arises with
`git merge` conflicts. The tool is optimized exactly for this case.

Use as follows:

```bash
   $ python3 tools/diffdumps.py -i base.json change1.json change2.json
```

This will allow you to interactively resolve conflicts that arise from two
diverging `git` branches.

The help text is reproduced here for completeness:

```bash
   $ python3 tools/diffdumps.py --help
   usage: diffdumps.py [-h] [-o OUTPUT] [-i] [-v] [--install] base first second

   Diff and merge django data dumps

   positional arguments:
     base        base for 3-way diff
     first       First file to compare
     second      Second file to compare

   optional arguments:
     -h, --help  show this help message and exit
     -o OUTPUT   Output of merge
     -i          Interactive resolution
     -v          Value conflicts: Only conflict if value differs (default:
                 conflict if any object is changed)
     --install   Install into Git config (repo-local)
```


## whichtest

`whichtest.py` - inspect coverage data

This utility allows you to inspect coverage data to find out which test
is covering which part of your code. Useful to figure out which tests to run
locally when you changed a particular piece of code.

Note: This requires up-to-date coverage data, which can be obtained by running
`pytest --cov`. If you don't have current coverage data, you may get errors, or
invalid output.

Usage:

* `python whichtest.py path/to_some_file.py`
* `python whichtest.py path/to_some_file.py:123`

This will give you a list of test cases for the given file, or, if you pass
the line number as well, just for the given line.

* `python whichtest.py --check-locality`
* `python whichtest.py --check-locality [-v|--verbose]`

Output the test locality score: The number of lines that are covered, across
the code base, by a test within the same module / django app.

If you enable verbose mode, it will output every line that's not covered by
a "local" test.

Note that this is rather generic and certain cases are not caught correctly yet:
For example urls.py files may be re-imported by some tests, but also at django
startup, so they look like "foreign covered" in here despite being strictly
declarative/module-scope code only. This is a limitation of coverage.py.
