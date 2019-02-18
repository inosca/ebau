from os import path

import requests_mock
from django.urls import reverse


def test_get_data(client, snapshot):
    with requests_mock.Mocker() as m:
        egrid = "CH643546955207"
        multisurface_file = open(
            path.join(path.dirname(__file__), "multisurface.xml"), "r"
        )
        m.get(
            """https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer?service=wfs&version=2.0.0&Request=GetFeature&typename=a42geo_a42geo_ortsangabenwfs_d_fk:DIPANU_DIPANUF&count=10&Filter=%3Cogc:Filter%3E%3Cogc:PropertyIsEqualTo%20matchCase=%22true%22%3E%3Cogc:PropertyName%3EEGRID%3C/ogc:PropertyName%3E%3Cogc:Literal%3E{0}%3C/ogc:Literal%3E%3C/ogc:PropertyIsEqualTo%3E%3C/ogc:Filter%3E""".format(
                egrid
            ),
            text=multisurface_file.read(),
        )
        response_file = open(path.join(path.dirname(__file__), "response.xml"), "r")
        m.post(
            """https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer""",
            text=response_file.read(),
        )

        response = client.get(reverse("egrid", kwargs={"egrid": egrid}))
        snapshot.assert_match(response.json())
