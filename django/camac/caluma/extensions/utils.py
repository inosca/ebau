def build_url(*fragments, **options):
    separator = options.get("separator", "/")

    url = separator.join([fragment.strip(separator) for fragment in fragments])

    if options.get("trailing", False):
        url += separator

    return url
