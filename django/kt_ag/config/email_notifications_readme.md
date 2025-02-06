# Disclaimer about IDs in `email_notifications.json`

Email notifications and snippets (notification templates of the type
"textcomponents") use the same table. While the email notifications are static
and managed by us, snippets are managed by the users themselves. In order to
avoid overwriting an existing snippet of a user because we add a new email
notification in the future, we added a notification template with the ID 100.
This will cause the ID sequence for snippets to start at 101 and give us some
room for future email notifications in the ID range between 1 and 100.

To avoid this problem completely, we should either split this functionality into
two separate models or get rid of the ID completely in favor of an already
existing slug. Currently this is not worth the effort as we still have old PHP
code which relies on notification template IDs. As soon as PHP is completely
dropped, we can and should refactor this onto one of the mentioned solutions.
