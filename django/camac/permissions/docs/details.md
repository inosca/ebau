# Permissions module - Implementation details & Notes


## Querying Cases

When listing cases, or case-related data, it should be sufficient to join the
ACLs to see whether a case is visible to the user. This can be done on database
level with minimal overhead.

Once a dossier is loaded and "visible", the full set of ACLs and associated permissions
should be loaded as well.


## Querying global case-dependent data

Some data is attached to a case, but is still listable "globally". For example,
work items from Caluma, or messages from the communications module. These have their
own rules, and cannot simply inherit the visibility rules of the ACLs (so, having an
ACL on a case does not give you read permissions on all the messages in that context, or
all the work items).

For this, the affected queryset is filtered first by the presence of an ACL as usual,
followed by further filtering as needed (involved parties for messages, created-by/assignee
value for work items, etc). So the query complexity is still reduced regarding access to
any given dossier's context, but not neccessarily in the narrowing-down part.

## Querying case-dependent data in a case context

Data that is only ever looked at in the scope of a single dossier/case can be filtered by
fetching the user's permissions in that dossier, and checking the specific entries required
to see a certain bit of information.

## Caching

Permissions do not change too quickly. Therefore, some medium-term caching
can be have a great impact on the subsystem's performance. The cache is
therefore used heavily to speed up permissions checking and listing.

See [Caching](./caching.md) for more details on this.
