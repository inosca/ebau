import logging
import xml.etree.ElementTree as ET

import requests


class EBauSoapClient:  # pragma: no cover
    """
    Client to load long texts from SAP using a SOAP endpoint.

    SAP stores multiline texts outside HANA DB. These only can be retrieved by the means of SAP functions.
    The used SOAP service allows to retrieve those texts .
    """

    def __init__(self, soap_server, soap_user, soap_password):
        self.soap_url = f"http://{soap_server}:50000/XISOAPAdapter/MessageServlet?senderParty=&senderService=EBP_Out&receiverParty=&receiverService=&interface=Gesuch_Out&interfaceNamespace=urn:ag.ch:KTAG_CRM_EBP:Gesuch"
        self.auth = (soap_user, soap_password)
        self.headers = {
            "Content-Type": "application/soap+xml",
            "Accept-Encoding": "gzip,deflate",
        }

    def get_dossier_texts(self, gesuch_id: str) -> dict[str, str]:
        soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <SOAP-ENV:Header>
                <WSCorIDSOAPHeader xmlns="http://www.ca.com/apm" />
            </SOAP-ENV:Header>
            <SOAP-ENV:Body>
                <yq1:Gesuch_Request_Access xmlns:yq1="urn:ag.ch:KTAG_CRM_EBP:Gesuch">
                    <accessType>RO</accessType>
                    <ges_id>{gesuch_id}</ges_id>
                </yq1:Gesuch_Request_Access>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""
        try:
            response = requests.post(
                self.soap_url, data=soap_body, headers=self.headers, auth=self.auth
            )
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.text)

            tags = [
                "bsguid_txt",
                "prguid_txt",
                "ghguid_txt",
                "blguid_txt",
                "maguid_txt",
                "gwguid_txt",
                "bkguid_txt",
            ]
            return {tag.upper(): self._extract_tag_value(root, tag) for tag in tags}

        except requests.RequestException as e:
            logging.warning(f"SOAP request failed: {e}")
        except ET.ParseError as e:
            logging.warning(f"Failed to parse SOAP response: {e}")

        return {}

    def _extract_tag_value(self, root, tag):
        txt_element = root.find(f".//{tag}")
        value = None
        if txt_element is not None:
            value = txt_element.text

        return value
