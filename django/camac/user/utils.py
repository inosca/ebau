def unpack_service_emails(queryset):
    """
    Extract email addresses for services.

    The email field can be used as a comma-separated list.
    This accessor returns the email addresses as a flat list.
    """

    for emails in queryset.values_list("email", flat=True):
        if not emails:
            return []

        yield from emails.split(",")
