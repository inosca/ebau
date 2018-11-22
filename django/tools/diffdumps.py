#!/usr/bin/env python3

"""Diff and merge multiple Django data dumps. """

from collections import defaultdict
import argparse
import json
import codecs
import sys


class Diffy():
    """Utility for comparing and merging JSON dumps from Django (dumpdata)"""

    class _NE:
        """Dummy for dict.get() that will always return False in comparison

        We use this to ensure non-existing values in one dict yield a
        difference as well.  This allows easier comparison even if the stored
        value is `None`, which might be a vaild entry as a database value.
        """
        def __eq__(self, other):
            return False

    def __init__(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        """Initialize new diffy tool.

        The file handles stdin, stderr, stdout may be routed as appropriate,
        depending on interactive or non-interactive use etc.
        """
        self.merged         = defaultdict(dict)
        self.conflicts      = []
        self.changes        = defaultdict(dict)
        self.sources        = []

        self.stdin  = stdin
        self.stdout = stdout
        self.stderr = stderr

    def _change_key(self, obj):
        return (obj['model'], obj['pk'])

    def _record_change(self, change, update):
        obj, source = update
        self.changes[change][source] = obj

    def _can_change(self, change):
        return len(self.changes[change]) == 0

    def apply_dump(self, newdata, source='input'):
        """Apply a django dumpdata file into the algorithm."""
        self.sources.append(source)

        for obj in newdata:
            self._apply_obj(obj, source)

    def _apply_obj(self, obj, source='input'):
        pk    = obj['pk']
        model = obj['model']

        change = self._change_key(obj)

        existing = self.merged[model].get(pk)

        if existing and self.equals(existing, obj):
            return
        self._record_change(change, (obj, source))

    def equals(self, first, second):
        """Compare two dicts."""
        ne = Diffy._NE()

        for key, val in first['fields'].items():
            if second['fields'].get(key, ne) != val:
                return False

        for key, val in second['fields'].items():
            if first['fields'].get(key, ne) != val:
                return False

        return True

    def _merged_objs(self):
        """Yield all merged objects in order."""
        for m in sorted(self.merged.keys()):
            for o in sorted(self.merged[m].keys()):
                yield self.merged[m][o]

    def flatten_changes(self):
        """Apply recorded changes if possible.

        Sort the changes into the merged result, if possible, otherwise
        record the change as a conflict.
        """
        for key, changeset in self.changes.items():
            model, pk = key

            is_conflict, obj = self._resolve(changeset)
            if is_conflict:
                self.conflicts.append(obj)
            else:
                self.merged[model][pk] = obj

        self.changes.clear()

    def _resolve(self, changeset):
        # Resolution table, assuming three inputs. X == Not existing, A, B, C
        # means differing values (A, A would be two equal values, A, B would
        # mean two differing values etc)
        #
        # CASE  Base   First  Second  RESULT   Notes
        #  (1)    X      X      X       X       invalid
        #  (2)    X      X      A       A
        #  (3)    X      A      X       A
        #  (4)    X      A      A       A
        #  (5)    X      A      B      Conflict

        #  (6)    A      X      X       X
        #  (7)    A      X      A       X
        #  (8)    A      X      B      Conflict

        #  (9)    A      A      X       X
        # (10)    A      A      A       A       happy :)
        # (11)    A      A      B       B

        # (12)    A      B      X      Conflict
        # (13)    A      B      A       B
        # (14)    A      B      B       B
        # (15)    A      B      C      Conflict

        # We assume three inputs, two-input mode should be specified when
        # needed
        assert len(self.sources) == 3, "Only 3-way compare is implemented now"

        b, f, s = [
            changeset.get(src, None)
            for src in self.sources
        ]

        CONFLICT = (True, changeset)
        OK       = lambda val: (False, val)

        if b is None:
            if f is None:
                return OK(s)                           # case 2
            elif s is None:
                return OK(f)                           # case 3
            elif self.equals(f, s):
                return OK(f)                           # case 4
            else:
                return CONFLICT                        # case 5
        elif f is None:
            if s is None:
                return OK(s)                           # case 6
            if self.equals(b, s):
                return OK(b)                           # case 7
            else:
                return CONFLICT                        # case 8
        elif self.equals(b, f):
            if s is None:
                return OK(s)                           # case 9
            elif self.equals(f, s):
                return OK(s)                           # case 10
            else:
                return OK(s)                           # case 11
        else:
            # first, validate assumptions
            assert(b is not None)
            assert(f is not None)
            assert(not self.equals(b, f))
            if s is None:
                return CONFLICT                        # case 12
            if self.equals(b, s) or self.equals(f, s):
                return OK(f)                           # cases 13, 14
            else:
                return CONFLICT                        # case 15

    def _resolve_conflict_interactive(self, conflict):
        # Excerpt from the resolution table in _resolve(). Only the "conflict"
        # cases are of interest here; the result is what we should present to
        # the user
        #
        # CASE  Base   First  Second  RESULT   Notes
        #  (5)    X      A      B     Two additions, likely we want to keep one
        #                             of them
        #  (8)    A      X      B     Modification and deletion: which one?
        # (12)    A      B      X     Modification and deletion: which one?
        # (15)    A      B      C     Two modifications

        if conflict.get('base') is None:  # case 5
            message = 'Two additions'
            choices = (
                ('f', 'Use first',  lambda: conflict['first']),
                ('s', 'Use second', lambda: conflict['second']),
                ('m', 'Merge f/s',  lambda: self._edit_conflict(conflict['first'], conflict['second'])),
                ('d', 'Drop both',  lambda: None),
            )
        elif conflict.get('first') is None:  # case 8
            message = "Deleted in 'first', modified in 'second'"
            choices = (
                ('s', 'Use second', lambda: conflict.get('second')),
                ('d', 'Drop',       lambda: None),
            )
        elif conflict.get('second') is None:  # case 12
            message = "Modified in 'first', deleted in 'second'"
            choices = (
                ('s', 'Use first', lambda: conflict.get('first')),
                ('d', 'Drop',      lambda: None),
            )
        else:
            message = "Modified in both 'first' and 'second'"
            choices = (
                ('b', 'Use base',     lambda: conflict['base']),
                ('f', 'Use first',    lambda: conflict['first']),
                ('s', 'Use second',   lambda: conflict['second']),
                ('m', 'Merge f/s',    lambda: self._edit_conflict(conflict['first'], conflict['second'])),
                ('d', 'Drop both',    lambda: None),
            )

        print("########## %s" % message, file=self.stderr)
        self._show_conflict(conflict, self.stderr)

        model, pk = self._key_from_conflict(conflict)

        resolved = self._interact(
            "How should I handle the conflict?", choices)

        if resolved is not None:
            self.merged[model][pk] = resolved

    def _key_from_conflict(self, conflict):
        """Return (model, pk) tuple from a conflict dict."""
        model = list(conflict.values())[0]['model']
        pk    = list(conflict.values())[0]['pk']
        return (model, pk)

    def _edit_conflict(self, cad, cbd):
        cas = 'first'
        cbs = 'second'

        def _show_val(loc, lname, key):
            if key in loc:
                self._print_e(
                    "  Value in %s: %s\n" % (
                        lname, json.dumps(loc[key])
                    )
                )
            else:
                self._print_e("  Missing in %s\n" % '.'.join(lname))

        keys_a = cad['fields'].keys()
        keys_b = cbd['fields'].keys()

        dict_a = cad['fields']
        dict_b = cbd['fields']

        all_keys = sorted(set(keys_a) | set(keys_b), key=lambda x: len(x))

        res = {}

        for key in all_keys:
            self._print_e("Merging in key '%s'\n" % key)

            if dict_a.get(key, Diffy._NE()) == dict_b.get(key, Diffy._NE()):
                self._print_e("  Values in %s and %s are equal: %s\n" % (
                    cas, cbs, json.dumps(dict_a[key])
                ))

                options = (
                    ('a', 'Accept', lambda: res.update({key: dict_b[key]})),
                    ('s', 'Skip',   lambda: True),
                )
            else:
                _show_val(dict_a, cas, key)
                _show_val(dict_b, cbs, key)
                options = (
                    ('f', 'Take first',    lambda: res.update({key: dict_a[key]})),
                    ('s', 'Take second',   lambda: res.update({key: dict_b[key]})),
                    ('i', 'Ignore (skip)', lambda: True),
                )

            self._interact("What to do?", options)

            self._print_e("OK, current state: %s\n" % json.dumps(res, indent=2))

        return {
            'model': cad['model'],
            'pk': cad['pk'],
            'fields': res
        }

    def resolve_interactive(self):
        """Interactively resolve the conflicts (if any)."""
        for conflict in self.conflicts:
            self._resolve_conflict_interactive(conflict)

        json.dump(list(self._merged_objs()), self.stdout, indent=2)

    def _print_e(self, *args):
        return print(*args, file=self.stderr)

    def _show_conflict(self, conflict, output):

        if conflict.get('base') is None:  # case 5
            message = 'Two additions'
        elif conflict.get('first') is None:  # case 8
            message = "Deleted in 'first', modified in 'second'"
        elif conflict.get('second') is None:  # case 12
            message = "Modified in 'first', deleted in 'second'"
        else:
            message = "Modified in both 'first' and 'second'"

        model, pk = self._key_from_conflict(conflict)

        print("########## Conflict (%s)" % message, file=output)
        print('{', file=output)
        print('   "model": "%s",' % model, file=output)
        print('   "pk": %d,' % pk,         file=output)

        for k in sorted(conflict.keys()):
            print("    # %s" % k, file=output)
            dump = json.dumps(conflict.get(k)['fields'], indent=2)
            print('    %s' % dump.replace('\n', '\n    '), file=output)

            print("\n", file=output)
        print('}', file=output)

    def _json_dump(self, data, fd):
        json.dump(data, fd, indent=2)
        fd.flush()

    def _interact(self, text, choices):
        while True:
            option_texts = [
                '[%s] %s' % (key, option)
                for key, option, action in choices
            ]
            self.stderr.write("%s %s " % (text, ', '.join(option_texts)))
            self.stderr.flush()

            inp = self.stdin.readline().strip().lower()
            print("\n", file=self.stderr)

            actions = [
                action
                for key, _, action
                in choices
                if key == inp
            ]

            try:
                # IndexError if user entered invalid choice is intended and
                # handled below
                action = actions[0]
                return action()
            except IndexError:
                self._print_e("Invalid choice, try again\n")
                pass
            except KeyboardInterrupt:
                self._print_e("Aborted, try again\n")
                pass

    def dump(self):
        """Dump the merged result to output, display conflicts afterwards.
        """

        # First, filter out the conflicting objects from the output
        for conflict in self.conflicts:
            model, pk = self._key_from_conflict(conflict)

            # don't show conflicting objects in "merged" output
            if pk in self.merged[model]:
                del self.merged[model][pk]

        # Second, dump the non-conflicting content
        json.dump(list(self._merged_objs()), self.stdout, indent=2)
        self.stdout.write("\n")

        # Last, dump the conflicts
        has_conflict = False
        for conflict in self.conflicts:
            has_conflict = True
            self._show_conflict(conflict, self.stdout)

        self.stdout.flush()

        if has_conflict:
            self._print_e("\nNOTE: CONFLICTS WRITTEN TO OUTPUT, PLEASE FIX MANUALLY!\n")
        else:
            self._print_e("\nNote: No conflicts, you're good to go!\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Diff and merge django data dumps')
    parser.add_argument('base',   nargs=1, type=argparse.FileType('r'), help='base for 3-way diff')
    parser.add_argument('first',  nargs=1, type=argparse.FileType('r'), help='First file to compare')
    parser.add_argument('second', nargs=1, type=argparse.FileType('r'), help='Second file to compare')
    parser.add_argument('-o',     nargs=1, type=argparse.FileType('w'), help='Output of merge', dest='output')
    parser.add_argument('-i',     action='store_true', help='Interactive resolution', dest='interactive')
    parser.add_argument('--install', action='store_true', help='Install into Git config (repo-local)', dest='install')

    if '--install' in sys.argv:
        # apart from the regular parsing, as the parser enforces the diff input files
        import subprocess
        subprocess.run(['git', 'config', '--local', 'mergetool.jsondiff.cmd', 'python3 %s $BASE $LOCAL $REMOTE -i -o $MERGED' % sys.argv[0]])
        subprocess.run(['git', 'config', '--local', 'mergetool.jsondiff.trustExitCode', 'true'])
        exit(0)

    args = parser.parse_args()

    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr
    if args.output:
        stdout = args.output[0]

    diffy = Diffy(
        stdin=stdin,
        stdout=stdout,
        stderr=stderr)

    diffy.apply_dump(json.load(args.base[0]),   'base')
    diffy.apply_dump(json.load(args.first[0]),  'first'),
    diffy.apply_dump(json.load(args.second[0]), 'second'),

    diffy.flatten_changes()

    if args.interactive:
        diffy.resolve_interactive()

    else:
        diffy.dump()
