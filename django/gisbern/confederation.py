import requests
from django.conf import settings
from django.core.cache import cache

from gisbern.views import get_root

#  this is currently unused, but left if the repository because it will be needed soon


def get_data(multisurface):
    xml_bund = """<GetFeature xmlns="http://www.opengis.net/wfs" xmlns:a42geo_ebau_bund_wfs_d_fk="http://www.geoservice.apps.be.ch/geoservice/services/a4p/a42geo_ebau_bund_wfs_d_fk/MapServer/WFSServer" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" service="WFS" version="2.0.0" outputFormat="GML2" count="100">
      <Query typeName="a42geo_ebau_bund_wfs_d_fk:MOORLAND_ML" srsName="EPSG:2056">
        <ogc:Filter>
          <ogc:Intersects>
            <ogc:PropertyName>Shape</ogc:PropertyName>
            {0}
          </ogc:Intersects>
        </ogc:Filter>
      </Query>
    </GetFeature>""".format(
        multisurface
    )

    request_bund = requests.post(
        "https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_bund_wfs_d_fk/MapServer/WFSServer?service=wfs&version=2.0.0&Request=GetCapabilities&token={0}".format(
            get_token()
        ),
        data=xml_bund,
        cookies={},
    )

    root_bund = get_root(request_bund)

    tag_list = []
    data = {}
    tags = {}

    # If featureMember layers are empty, the values are false
    if root_bund.findall("./{http://www.opengis.net/gml/3.2}featureMember/") == []:
        for key, value in tags.items():
            data[key] = value in tag_list

    # Find all layers beneath featureMember
    for child in root_bund.findall("./{http://www.opengis.net/gml/3.2}featureMember/"):
        tag_list.append(child.tag)

    # true/false values of bund service
    for key, value in tags.items():
        data[key] = value in tag_list


def get_token():
    if not settings.GIS_API_USERNAME or not settings.GIS_API_PASSWORD:
        raise ValueError("Please specify GIS_API_USERNAME and GIS_API_PASSWORD")

    # Token lifetime is 1 hour according to Pierre Honsberger (aDue)
    return cache.get_or_set("token", lambda _: request_new_token(), 3600)


def request_new_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    values = {
        "username": settings.GIS_API_USERNAME,
        "password": settings.GIS_API_PASSWORD,
        "f": "json",
    }
    request_token = requests.post(
        "https://www.geoservice.apps.be.ch/geoservice2/tokens/generateToken",
        data=values,
        headers=headers,
    )
    return request_token.json()["token"]
