from os import path

import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from lxml import etree
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from camac.utils import build_url

_session = requests.session()


@swagger_auto_schema(method="get", auto_schema=None)
@api_view(["GET"])
@permission_classes([])
def gis_data_view(request, egrid, format=None):
    # View to list all the data from the GIS service.
    try:
        return Response(get_gis_data(get_polygon(egrid)))
    except ValueError as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


def get_polygon(egrid):
    """Get a polygon with the coordinates of a parcel.

    :param    egrid:    the number of a parcel
    :type     egrid:    str
    :return:            a polygon with the coordinates of a parcel
    :rtype:             str
    """

    response = _session.get(
        build_url(
            settings.GIS_BASE_URL,
            f"/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer?service=WFS&version=2.0.0&Request=GetFeature&typename=a42geo_a42geo_ebau_kt_wfs_d_fk:DIPANU_DIPANUF&count=10&Filter=%3Cogc:Filter%3E%3Cogc:PropertyIsEqualTo%20matchCase=%22true%22%3E%3Cogc:PropertyName%3EEGRID%3C/ogc:PropertyName%3E%3Cogc:Literal%3E{egrid}%3C/ogc:Literal%3E%3C/ogc:PropertyIsEqualTo%3E%3C/ogc:Filter%3E",
        )
    )

    try:
        root = get_root(response)
    except etree.XMLSyntaxError:
        raise ValueError("Can't parse document")

    try:
        polygon = root.find(".//gml:Polygon", root.nsmap)
        return etree.tostring(polygon, encoding="unicode")
    except (SyntaxError, TypeError):
        raise ValueError("No polygon found")


def get_gis_data(polygon):
    """Get the data from the GIS service.

    :param   polygon: a polygon with coordinates
    :type    polygon: str
    :return:          the data from the GIS service
    :rtype:           dict
    """

    all_boolean_layers = [
        "GEODB.GSK25_GSK_VW",  # Gewässerschutzzonen
        "BALISKBS_KBS",  # Belasteter Standort
        "GK5_SY",  # Naturgefahren
        "GEODB.BAUINV_BAUINV_VW",  # Bauinventar
        "GEODB.UZP_LSG_VW",  # Besonderer Landschaftsschutz
        "ARCHINV_FUNDST",  # Archäologische Fundstellen
        "NSG_NSGP",  # Naturschutzgebiet
    ]
    all_special_layers = [
        "GEODB.UZP_BAU_VW",  # Nutzungszone
        "GEODB.UZP_UEO_VW",  # Überbauungsordnung
    ]

    boolean_layers = [
        layer
        for layer in all_boolean_layers
        if layer not in settings.GIS_SKIP_BOOLEAN_LAYERS
    ]
    special_layers = [
        layer
        for layer in all_special_layers
        if layer not in settings.GIS_SKIP_SPECIAL_LAYERS
    ]

    query = "".join(
        map(
            lambda x: """<Query typeName="a42geo_ebau_kt_wfs_d_fk:{0}" srsName="EPSG:2056">
        <ogc:Filter>
          <ogc:Intersects>
            {1}
          </ogc:Intersects>
        </ogc:Filter>
      </Query>""".format(
                x, polygon
            ),
            boolean_layers + special_layers,
        )
    )

    get_feature_xml = open(
        path.join(path.dirname(__file__), "xml/get_feature.xml"), "r"
    ).read()

    response_kanton = _session.post(
        "{0}/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer".format(
            settings.GIS_BASE_URL
        ),
        data=get_feature_xml.format(baseURL=settings.GIS_BASE_URL, query=query),
    )

    try:
        et = get_root(response_kanton)
    except etree.XMLSyntaxError:
        raise ValueError("Can't parse document")

    tag_list = []
    data = {}

    usage_zones = set()
    building_regulations = set()
    water_protection_zones = set()

    # Find all layers beneath featureMember
    for child in et.findall("./gml:featureMember/", et.nsmap):
        tag_list.append(child.tag)

        # true/false values of kanton service
        for value in boolean_layers:
            data[value.split(".")[-1]] = len([x for x in tag_list if value in x]) > 0

        # Nutzungszone ([String])
        if "GEODB.UZP_BAU_VW" in child.tag:
            for item in child.findall(
                "a42geo_a42geo_ebau_kt_wfs_d_fk:ZONE_LO", et.nsmap
            ):
                usage_zones.add(item.text.strip())

        # Überbauungsordnung (String)
        if "GEODB.UZP_UEO_VW" in child.tag:
            for item in child.findall(
                "a42geo_a42geo_ebau_kt_wfs_d_fk:ZONE_LO", et.nsmap
            ):
                building_regulations.add(item.text.strip())

        # Gewässerschutz (String)
        for item in child.findall(
            "a42geo_a42geo_ebau_kt_wfs_d_fk:GSKT_BEZEICH_DE", et.nsmap
        ):
            water_protection_zones.add(item.text.strip())

    return {
        **data,
        "UZP_BAU_VW": sorted(usage_zones),
        "UZP_UEO_VW": sorted(building_regulations),
        "GSKT_BEZEICH_DE": sorted(water_protection_zones),
    }


def get_root(response):
    return etree.fromstring(response.content)
