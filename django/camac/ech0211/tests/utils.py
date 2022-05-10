from django.conf import settings


def xml_data(file_name, config="kt_bern"):
    with open(
        str(settings.ROOT_DIR(f"{config}/static/ech0211/xml/post/{file_name}.xml")), "r"
    ) as myfile:
        data = myfile.read()
    return data
