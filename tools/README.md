CAMAC-BE Tools collection
=========================

This directory is intended for various tools that support development.

Diffdumps
---------

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

<!-- vim:set syntax=markdown sw=3 ts=3 et tw=78: -->
