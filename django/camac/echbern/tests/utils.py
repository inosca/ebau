from django.conf import settings


def xml_data(file_name):
    with open(
        str(settings.ROOT_DIR(f"camac/echbern/static/xml/post/{file_name}.xml")), "r"
    ) as myfile:
        data = myfile.read()
    return data
