import xml.etree.ElementTree as ET

import requests_mock

from .views import get_multisurface, get_gis_data


def test_get_multisurface():
    with requests_mock.Mocker() as m:
        ET.register_namespace("gml", "http://www.opengis.net/gml/3.2")
        ET.register_namespace(
            "ogc",
            "http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer",
        )
        egrid = "CH643546955207"
        multisurface_file = open("gisbern/multisurface.txt", "r")
        m.get(
            """https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer?service=wfs&version=2.0.0&Request=GetFeature&typename=a42geo_a42geo_ortsangabenwfs_d_fk:DIPANU_DIPANUF&count=10&Filter=%3Cogc:Filter%3E%3Cogc:PropertyIsEqualTo%20matchCase=%22true%22%3E%3Cogc:PropertyName%3EEGRID%3C/ogc:PropertyName%3E%3Cogc:Literal%3E{0}%3C/ogc:Literal%3E%3C/ogc:PropertyIsEqualTo%3E%3C/ogc:Filter%3E""".format(
                egrid
            ),
            text=multisurface_file.read(),
        )
        assert (
            get_multisurface(egrid)
            == """<gml:MultiSurface srsName="urn:ogc:def:crs:EPSG:6.9:2056"><gml:surfaceMember><gml:Polygon><gml:exterior><gml:LinearRing><gml:posList>2609722.3770000003 1176042.1519999988</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:surfaceMember></gml:MultiSurface>"""
        )


def test_get_data():
    with requests_mock.Mocker() as m:
        ET.register_namespace("gml", "http://www.opengis.net/gml/3.2")
        ET.register_namespace(
            "ogc",
            "http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer",
        )
        multisurface = get_multisurface("CH643546955207")

        # assert (get_gis_data()
