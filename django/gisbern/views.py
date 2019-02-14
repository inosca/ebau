import xml.etree.ElementTree as ET

import requests
from django.core.cache import cache
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
            text = ET.tostring(child, encoding="unicode")
            text = text.replace(' xmlns:gml="http://www.opengis.net/gml/3.2"', "")
            return text

    def get_gis_data(multisurface):
        """Get the data from the GIS service.

        :param    multisurface:     a multisurface with coordinates
        :type     multisurface:     str
        :return:                    the data from the GIS service
        :rtype:                     dict
        """

        xml_kanton = """<GetFeature xmlns="http://www.opengis.net/wfs" xmlns:a42geo_ebau_kt_wfs_d_fk="http://www.geoservice.apps.be.ch/geoservice/services/a4p/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" service="WFS" version="2.0.0" outputFormat="GML2" count="100">
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:GEODB.UZP_BAU_VW" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:GEODB.UZP_UEO_VW" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:GEODB.GSK25_GSK_VW" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:BALISKBS_KBS" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:GK5_SY" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:GEODB.BAUINV_BAUINV_VW" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:GEODB.UZP_LSG_VW" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:ARCHINV_FUNDST" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:NSG_NSGP" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                <ogc:PropertyName>Shape</ogc:PropertyName>
                {0}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>
          <Query typeName="a42geo_ebau_kt_wfs_d_fk:STREU_STREU" srsName="EPSG:2056">
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

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        values = {
            "username": "a42geo_ebau_user",
            "password": "a4p_7aaWb5zWgYByJ2j",
            "f": "json",
        }
        if not cache.get("token"):
            request_token = requests.post(
                "https://www.geoservice.apps.be.ch/geoservice2/tokens/generateToken",
                data=values,
                headers=headers,
            )
            token = request_token.json()["token"]
            cache.set("token", token, 3600)
        request_kanton = requests.post(
            "https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer",
            data=xml_kanton,
        )
        request_bund = requests.post(
            "https://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_ebau_bund_wfs_d_fk/MapServer/WFSServer?service=wfs&version=2.0.0&Request=GetCapabilities&token={0}".format(
                cache.get("token")
            ),
            data=xml_bund,
            cookies={},
        )
        request_kanton.encoding = "UTF-8"
        request_bund.encodig = "UTF-8"
        body_kanton = request_kanton.text
        body_bund = request_bund.text
        root_kanton = ET.fromstring(body_kanton)
        root_bund = ET.fromstring(body_bund)
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

        # If featureMember layers are empty, the values are false
        if root_bund.findall("./{http://www.opengis.net/gml/3.2}featureMember/") == []:
            for key, value in tags.items():
                data[key] = value in tag_list

        # Find all layers beneath featureMember
        for child in root_bund.findall(
            "./{http://www.opengis.net/gml/3.2}featureMember/"
        ):
            tag_list.append(child.tag)

            # true/false values of bund service
            for key, value in tags.items():
                data[key] = value in tag_list

        # Find all layers beneath featureMember
        for child in root_kanton.findall(
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
                for item in child.findall(
                    "./{http://x3012app435.infra.be.ch:6080/arcgis/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer}ZONE_LO"
                ):
                    data["nutzungszone"] = item.text

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

    multisurface = get_multisurface(egrid)
    data = get_gis_data(multisurface)
    return Response(data)
