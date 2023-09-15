# Permissions module - Caching

Permissions do not change too quickly. Therefore, some medium-term caching
can be have a great impact on the subsystem's performance. The cache is
therefore used heavily to speed up permissions checking and listing.

When ACL information for a user/case is not yet cached, the cache expiry
is set to the earliest date where an ACL expires. In addition, every time an
ACL is created or revoked, all ACL cache entries for the affected case are
evicted.

A single user may access the system under various roles: Either as a member of the
public (but authenticated), as a member of staff (internal), or as a viewer
of publicised data (unauthenticated, optionally authorized by a invitation via token)

Inosca discriminates between these accesses by optionally passing a
custom HTTP header to identify the currently-active group a user is using.
All access is then restricted to that given group. Without that header, the
user is considered member-of-the-public, who use the system to manage
and submit their own building permits.


