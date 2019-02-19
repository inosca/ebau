from os import path

import requests
from lxml import etree
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([])
def gis_data_view(request, egrid, format=None):
    # View to list all the data from the GIS service.
    try:
        multisurface = get_multisurface(egrid)
        return Response(get_gis_data(multisurface))
    except ValueError as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


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

    root = etree.fromstring(request.text)
    try:
        multisurface = root.find(".//gml:MultiSurface", root.nsmap)
        return etree.tostring(multisurface, encoding="unicode").replace(
            ' xmlns:gml="http://www.opengis.net/gml/3.2"', ""
        )
    except (SyntaxError, TypeError):
        raise ValueError("No multisurface found")


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
        "belasteter_standort": "BALISKBS_KBS",
        "gebiet_mit_naturkatastrophen": "GK5_SY",
        "besonderer_landschaftsschutz": "GEODB.UZP_LSG",
        "archäologisches_objekt": "ARCHINV_FUNDS",
        "naturschutzgebiet": "NSG_NSGP",
        "bauinventar": "GEODB.BAUINV.BAUINV_VW",
    }

    et = get_root(request_kanton)
    # Find all layers beneath featureMember
    for child in et.findall("./{http://www.opengis.net/gml/3.2}featureMember/"):
        tag_list.append(child.tag)

        # true/false values of kanton service
        for key, value in tags.items():
            data[key] = len([x for x in tag_list if value in x]) > 0

        # text values
        if "GEODB.UZP_BAU_VW" in child.tag:
            zones = []
            for item in child.findall(
                "a42geo_a42geo_ebau_kt_wfs_d_fk:ZONE_LO", et.nsmap
            ):
                zones.append(item.text)
                data["nutzungszone"] = zones

        if "GEODB.UZP_UEO_VW" in child.tag:
            for item in child.findall(
                "a42geo_a42geo_ebau_kt_wfs_d_fk:ZONE_LO", et.nsmap
            ):
                data["überbauungsordnung"] = item.text

        for item in child.findall(
            "a42geo_a42geo_ebau_kt_wfs_d_fk:GSKT_BEZEICH_DE", et.nsmap
        ):
            data["gewässerschutz"] = item.text
    return data


def get_root(request):
    request.encoding = "UTF-8"
    return etree.fromstring(request.text)
