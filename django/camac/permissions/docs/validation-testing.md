# Permissions module - Validation & Testing

The permissions system is a critical part of the whole application: It defines
who, under which conditions, may see certain data, or may perform certain actions.

Dropping any permission that a user rightfully has leads to unneccessary churn
and unhappiness.

Granting any permisison that a user does *not* rightfully possess leads to
data leaks and potential legal trouble, in addition to any unhappiness.

Worse, any such leak may not be detected during regular testing, either manual
or automatic, as testing can never cover everything 100%.

## Possible validation strategies

There are a few validation strategies to ensure the new permission system
behaves exactly as the old one did. Some are more practical than others,
and some will require complex systems and/or automations.

Generally speaking, there are two types of strategies we need to consider:

- Switching Systems: Both permissions systems need to be accessible somehow,
  so the behaviour can be compared
- Testing agent: A comparison system needs to exist that can access both
  versions and compare them


## General validation setup

Any validation setup needs to perform the following steps:

1. Setup situation
2. Perform test scenario
3. Record results
4. Compare results

Steps 1-3 need to be performed on both systems. Any discrepancy in step 4 needs
to be accounted for as either intentional, or as a bug.

## Permission system switch

### Time-based switching

This is, from a programming perspective, the easiest: We document all the affected API
endpoints at a given point in time. Then, when the new system is in place, we perform
the same actions, in the same situations (ideally with the same data), using the new
system and note any differences.

This is akin to what the `pytest-snapshottest` module is doing. 

PROS: Reduced resources, fast, easy to implement
CONS: No retroactive addition of test cases

### Parallel systems

In this scenario, both versions of the code run on parallel, independent systems.
One is using the new permissions module (perhaps using the feature branch), the other
is using the old code (main/master branch).

A testing agent can then perform the same actions, in parallel, on both systems, and
note any differences.

PROS: fast, relatively easy to implement, retroactive test cases possible 
CONS: requires additional compute resources

### Feature-Flags

Here, we use feature flags in the code to activate one or the other permissions
system. The flags may be activated via query parameters or env variables.

The testing agent can switch between them using appropriate tooling, then compare
the behaviour and note any differences.

PROS: Reduced resources, fast
CONS: high code complexity, need to test the switching-system as well

## Testing Agents

### Manual testing

This involves a complex test script, explaining exactly what to perform and
under which user / role certain actions should be possible or not, and under
which circumstances certain data should be visible or not.

PROS: simple, fast when no repetition required
CONS: error-prone, when many iterations required becomes slow

### Automated "unit" testing

Here, we would implement a set of additional "snapshot" tests that cover more
of the permission system's aspects. The configurations / situations would still
need manual work to setup however. 

PROS: simple, known tools, easy
CONS: may be incomplete, testing code needs to be separate from feature code
      so it can be run against both variants

### Fuzzing agent

A fuzzing agent is given a list of API endpoints and automates fetching data
and performing actions by exhaustively testing all endpoints, using a set of
user / role combinations. The output of the test is again a script that would
be reproducible in a new system.

PROS: relatively simple, may cover widest range of endpoints/behaviours
CONS: 

##  Promising strategy combinations

