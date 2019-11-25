def xml_encode_newlines(value):
    if not isinstance(value, str):
        return value

    replace_map = (("\n", "&#10;"), ("\r", "&#13;"))
    for old, new in replace_map:
        value = value.replace(old, new)

    return value
