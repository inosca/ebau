import xml.etree.ElementTree as ET
from os import path

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([])
def gis_data_view(request, egrid, format=None):
    # View to list all the data from the GIS service.

    ET.register_namespace("gml", "http://www.opengis.net/gml/3.2")
    ET.register_namespace(
        "ogc",
        "http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer",
    )
    multisurface = get_multisurface(egrid)
    data = get_gis_data(multisurface)
    return Response(data)


def get_multisurface(egrid):
    """Get a multisurface with the coordinates of a parcel.

    :param    egrid:    the number of a parcel
    :type     egrid:    str
    :return:            a multisurface with the coordinates of a parcel
    :rtype:             str
    """

    request = requests.get(
        """https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer?service=wfs&version=2.0.0&Request=GetFeature&typename=a42geo_a42geo_ortsangabenwfs_d_fk:DIPANU_DIPANUF&count=10&Filter=%3Cogc:Filter%3E%3Cogc:PropertyIsEqualTo%20matchCase=%22true%22%3E%3Cogc:PropertyName%3EEGRID%3C/ogc:PropertyName%3E%3Cogc:Literal%3E{0}%3C/ogc:Literal%3E%3C/ogc:PropertyIsEqualTo%3E%3C/ogc:Filter%3E""".format(
            egrid
        )
    )

    body = request.text
    root = ET.fromstring(body)
    for child in root.iter("{http://www.opengis.net/gml/3.2}MultiSurface"):
        # remove namespace from response to allow reuse in next request
        return ET.tostring(child, encoding="unicode").replace(
            ' xmlns:gml="http://www.opengis.net/gml/3.2"', ""
        )


def get_gis_data(multisurface):
    """Get the data from the GIS service.

    :param    multisurface:     a multisurface with coordinates
    :type     multisurface:     str
    :return:                    the data from the GIS service
    :rtype:                     dict
    """

    layers = [
        "GEODB.UZP_BAU_VW",
        "GEODB.UZP_UEO_VW",
        "GEODB.GSK25_GSK_VW",
        "BALISKBS_KBS",
        "GK5_SY",
        "GEODB.BAUINV_BAUINV_VW",
        "GEODB.UZP_LSG_VW",
        "ARCHINV_FUNDST",
        "NSG_NSGP",
    ]

    query = list(
        map(
            lambda x: """<Query typeName="a42geo_ebau_kt_wfs_d_fk:{0}" srsName="EPSG:2056">
        <ogc:Filter>
          <ogc:Intersects>
            <ogc:PropertyName>Shape</ogc:PropertyName>
            {1}
          </ogc:Intersects>
        </ogc:Filter>
      </Query>)""".format(
                x, multisurface
            ),
            layers,
        )
    )

    get_feature_xml = open(
        path.join(path.dirname(__file__), "xml/get_feature.xml"), "r"
    ).read()
    xml_kanton = get_feature_xml.format(query)

    request_kanton = requests.post(
        "https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer",
        data=xml_kanton,
    )

    tag_list = []
    data = {}
    tags = {
        "belasteter_standort": "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}BALISKBS_KBS",
        "gebiet_mit_naturkatastrophen": "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}GK5_SY",
        "besonderer_landschaftsschutz": "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}GEODB.UZP_LSG",
        "archäologisches_objekt": "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}ARCHINV_FUNDS",
        "naturschutzgebiet": "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}NSG_NSGP",
        "bauinventar": "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}GEODB.BAUINV.BAUINV_VW",
    }

    # Find all layers beneath featureMember
    for child in get_root(request_kanton).findall(
        "./{http://www.opengis.net/gml/3.2}featureMember/"
    ):
        tag_list.append(child.tag)

        # true/false values of kanton service
        for key, value in tags.items():
            data[key] = value in tag_list

        # text values
        if (
            child.tag
            == "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}GEODB.UZP_BAU_VW"
        ):
            zones = []
            for item in child.findall(
                "./{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}ZONE_LO"
            ):
                zones.append(item.text)
                data["nutzungszone"] = zones

        if (
            child.tag
            == "{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}GEODB.UZP_UEO_VW"
        ):
            for item in child.findall(
                "./{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}ZONE_LO"
            ):
                data["überbauungsordnung"] = item.text

        for item in child.findall(
            "./{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}GSKT_BEZEICH_DE"
        ):
            data["gewässerschutz"] = item.text
    return data


def get_root(request):
    request.encoding = "UTF-8"
    return ET.fromstring(request.text)
