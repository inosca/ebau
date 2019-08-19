from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView

from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance

XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <ns2:delivery xmlns:ns2="http://www.ech.ch/xmlns/eCH-0211/2" xmlns:ns4="http://www.ech.ch/xmlns/eCH-0010/6" xmlns:ns3="http://www.ech.ch/xmlns/eCH-0129/5" xmlns:ns6="http://www.ech.ch/xmlns/eCH-0044/4" xmlns:ns5="http://www.ech.ch/xmlns/eCH-0007/6" xmlns:ns8="http://www.ech.ch/xmlns/eCH-0008/3" xmlns:ns7="http://www.ech.ch/xmlns/eCH-0097/2" xmlns:ns13="http://www.ech.ch/xmlns/eCH-0046/1" xmlns:ns9="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:ns12="http://www.ech.ch/xmlns/eCH-0044/1" xmlns:ns11="http://www.ech.ch/xmlns/eCH-0147/T0/1" xmlns:ns10="http://www.ech.ch/xmlns/eCH-0039/2" xmlns:ns15="http://www.ech.ch/xmlns/eCH-0058/3" xmlns:ns14="http://www.ech.ch/xmlns/eCH-0010/3">
    <ns2:deliveryHeader>
      <ns9:senderId>gemdat://test-123</ns9:senderId>
      <ns9:messageId>797e3a7e-050c-4f40-aba8-3ff12fa4493b</ns9:messageId>
      <ns9:messageType>5100000</ns9:messageType>
      <ns9:sendingApplication>
        <ns9:manufacturer>GemDat Informatik AG</ns9:manufacturer>
        <ns9:product>eBaugesucheZH</ns9:product>
        <ns9:productVersion>1.0.0</ns9:productVersion>
      </ns9:sendingApplication>
      <ns9:messageDate>2019-08-19T00:00:00.000Z</ns9:messageDate>
      <ns9:action>1</ns9:action>
      <ns9:testDeliveryFlag>true</ns9:testDeliveryFlag>
    </ns2:deliveryHeader>
    <ns2:eventSubmitPlanningPermissionApplication>
      <ns2:eventType>submit</ns2:eventType>
      <ns2:planningPermissionApplication>
        <ns2:planningPermissionApplicationIdentification>
          <ns2:localID>
            <ns3:IdCategory>Category</ns3:IdCategory>
            <ns3:Id>ID</ns3:Id>
          </ns2:localID>
          <ns2:otherID>
            <ns3:IdCategory>Category</ns3:IdCategory>
            <ns3:Id>ID</ns3:Id>
          </ns2:otherID>
          <ns2:dossierIdentification>1111-111111-1111-11111111</ns2:dossierIdentification>
        </ns2:planningPermissionApplicationIdentification>
        <ns2:description>Hier sehen sie eine Beschreibung zum Bauprojekt.</ns2:description>
        <ns2:applicationType>nicht bekannt</ns2:applicationType>
        <ns2:remark>Remark</ns2:remark>
        <ns2:proceedingType>Ordentliches Verfahren</ns2:proceedingType>
        <ns2:profilingYesNo>true</ns2:profilingYesNo>
        <ns2:profilingDate>2019-08-19Z</ns2:profilingDate>
        <ns2:intendedPurpose>Wohnen</ns2:intendedPurpose>
        <ns2:parkingLotsYesNo>true</ns2:parkingLotsYesNo>
        <ns2:constructionCost>99999999.25</ns2:constructionCost>
        <ns2:locationAddress>
          <ns4:street>Eine lange Strasse</ns4:street>
          <ns4:houseNumber>233b</ns4:houseNumber>
          <ns4:town>St.Gallen</ns4:town>
          <ns4:swissZipCode>9000</ns4:swissZipCode>
        </ns2:locationAddress>
        <ns2:realestateInformation>
          <ns2:realestate>
            <ns3:realestateIdentification>
              <ns3:EGRID>CH940820788117</ns3:EGRID>
              <ns3:number>12345</ns3:number>
              <ns3:subDistrict>56789</ns3:subDistrict>
            </ns3:realestateIdentification>
            <ns3:realestateType>1</ns3:realestateType>
          </ns2:realestate>
          <ns2:municipality>
            <ns5:municipalityId>233</ns5:municipalityId>
            <ns5:municipalityName>Bonstetten</ns5:municipalityName>
            <ns5:cantonAbbreviation>ZH</ns5:cantonAbbreviation>
          </ns2:municipality>
          <ns2:buildingInformation>
            <ns2:building>
              <ns3:buildingIdentification>
                <ns3:street>Radhofstrasse</ns3:street>
                <ns3:houseNumber>23c</ns3:houseNumber>
                <ns3:zipCode>9000</ns3:zipCode>
                <ns3:cadasterAreaNumber>666</ns3:cadasterAreaNumber>
                <ns3:number>12345</ns3:number>
                <ns3:municipality>233</ns3:municipality>
              </ns3:buildingIdentification>
              <ns3:numberOfFloors>3</ns3:numberOfFloors>
              <ns3:numberOfSeparateHabitableRooms>6</ns3:numberOfSeparateHabitableRooms>
              <ns3:buildingCategory>1030</ns3:buildingCategory>
              <ns3:buildingClass>1110</ns3:buildingClass>
              <ns3:heating>
                <ns3:heatGeneratorHeating>7436</ns3:heatGeneratorHeating>
                <ns3:energySourceHeating>7530</ns3:energySourceHeating>
                <ns3:informationSourceHeating>852</ns3:informationSourceHeating>
                <ns3:revisionDate>2019-08-19Z</ns3:revisionDate>
              </ns3:heating>
              <ns3:hotWater>
                <ns3:heatGeneratorHotWater>7600</ns3:heatGeneratorHotWater>
                <ns3:energySourceHeating>7530</ns3:energySourceHeating>
                <ns3:informationSourceHeating>852</ns3:informationSourceHeating>
                <ns3:revisionDate>2019-08-19Z</ns3:revisionDate>
              </ns3:hotWater>
            </ns2:building>
            <ns2:dwelling>
              <ns3:administrativeDwellingNo>1234</ns3:administrativeDwellingNo>
              <ns3:noOfHabitableRooms>2</ns3:noOfHabitableRooms>
              <ns3:floor>1</ns3:floor>
              <ns3:multipleFloor>false</ns3:multipleFloor>
              <ns3:kitchen>true</ns3:kitchen>
              <ns3:surfaceAreaOfDwelling>90</ns3:surfaceAreaOfDwelling>
            </ns2:dwelling>
            <ns2:dwelling>
              <ns3:administrativeDwellingNo>1234</ns3:administrativeDwellingNo>
              <ns3:noOfHabitableRooms>4</ns3:noOfHabitableRooms>
              <ns3:floor>2</ns3:floor>
              <ns3:multipleFloor>true</ns3:multipleFloor>
              <ns3:kitchen>true</ns3:kitchen>
              <ns3:surfaceAreaOfDwelling>140</ns3:surfaceAreaOfDwelling>
            </ns2:dwelling>
          </ns2:buildingInformation>
          <ns2:placeName>
            <ns3:placeNameType>0</ns3:placeNameType>
            <ns3:localGeographicalName>Hinteremühle</ns3:localGeographicalName>
          </ns2:placeName>
          <ns2:owner>
            <ns2:ownerIdentification>
              <ns2:personIdentification>
                <ns6:officialName>Meier</ns6:officialName>
                <ns6:firstName>Hans</ns6:firstName>
              </ns2:personIdentification>
              <ns2:organisationIdentification>
                <ns7:organisationName>Muster-Organistaion</ns7:organisationName>
              </ns2:organisationIdentification>
            </ns2:ownerIdentification>
            <ns2:ownerAdress>
              <ns4:addressInformation>
                <ns4:street>Obere Strasse</ns4:street>
                <ns4:houseNumber>23</ns4:houseNumber>
                <ns4:town>Winterthur</ns4:town>
                <ns4:swissZipCode>2323</ns4:swissZipCode>
              </ns4:addressInformation>
            </ns2:ownerAdress>
          </ns2:owner>
        </ns2:realestateInformation>
        <ns2:realestateInformation>
          <ns2:realestate>
            <ns3:realestateIdentification>
              <ns3:EGRID>CH940820788118</ns3:EGRID>
              <ns3:number>12345</ns3:number>
              <ns3:subDistrict>56789</ns3:subDistrict>
            </ns3:realestateIdentification>
            <ns3:realestateType>1</ns3:realestateType>
          </ns2:realestate>
          <ns2:municipality>
            <ns5:municipalityId>233</ns5:municipalityId>
            <ns5:municipalityName>Bonstetten</ns5:municipalityName>
            <ns5:cantonAbbreviation>ZH</ns5:cantonAbbreviation>
          </ns2:municipality>
          <ns2:buildingInformation>
            <ns2:building>
              <ns3:buildingIdentification>
                <ns3:EGID>12346</ns3:EGID>
                <ns3:street>Radhofstrasse</ns3:street>
                <ns3:houseNumber>23d</ns3:houseNumber>
                <ns3:zipCode>9000</ns3:zipCode>
                <ns3:number>12346</ns3:number>
                <ns3:municipality>233</ns3:municipality>
              </ns3:buildingIdentification>
              <ns3:numberOfFloors>4</ns3:numberOfFloors>
              <ns3:numberOfSeparateHabitableRooms>7</ns3:numberOfSeparateHabitableRooms>
              <ns3:buildingCategory>1030</ns3:buildingCategory>
              <ns3:buildingClass>1110</ns3:buildingClass>
              <ns3:heating>
                <ns3:heatGeneratorHeating>7436</ns3:heatGeneratorHeating>
                <ns3:energySourceHeating>7530</ns3:energySourceHeating>
                <ns3:informationSourceHeating>852</ns3:informationSourceHeating>
                <ns3:revisionDate>2019-08-19Z</ns3:revisionDate>
              </ns3:heating>
              <ns3:hotWater>
                <ns3:heatGeneratorHotWater>7600</ns3:heatGeneratorHotWater>
                <ns3:energySourceHeating>7530</ns3:energySourceHeating>
                <ns3:informationSourceHeating>852</ns3:informationSourceHeating>
                <ns3:revisionDate>2019-08-19Z</ns3:revisionDate>
              </ns3:hotWater>
            </ns2:building>
            <ns2:dwelling>
              <ns3:administrativeDwellingNo>1234</ns3:administrativeDwellingNo>
              <ns3:noOfHabitableRooms>2</ns3:noOfHabitableRooms>
              <ns3:multipleFloor>false</ns3:multipleFloor>
              <ns3:surfaceAreaOfDwelling>80</ns3:surfaceAreaOfDwelling>
            </ns2:dwelling>
          </ns2:buildingInformation>
          <ns2:placeName>
            <ns3:placeNameType>0</ns3:placeNameType>
            <ns3:localGeographicalName>Hinteremühle</ns3:localGeographicalName>
          </ns2:placeName>
        </ns2:realestateInformation>
        <ns2:zone>
          <ns2:zoneDesignation>zoneDesignation</ns2:zoneDesignation>
        </ns2:zone>
        <ns2:constructionProjectInformation>
          <ns2:constructionProject>
            <ns3:typeOfConstructionProject>6011</ns3:typeOfConstructionProject>
          </ns2:constructionProject>
          <ns2:municipality>
            <ns5:municipalityId>233</ns5:municipalityId>
            <ns5:municipalityName>Bonstetten</ns5:municipalityName>
            <ns5:cantonAbbreviation>ZH</ns5:cantonAbbreviation>
          </ns2:municipality>
        </ns2:constructionProjectInformation>
        <ns2:document>
          <ns11:uuid>1111-111111-1111-11111111</ns11:uuid>
          <ns11:titles>
            <ns10:title ns10:lang="de">myFile.pdf</ns10:title>
          </ns11:titles>
          <ns11:status>created</ns11:status>
          <ns11:files>
            <ns11:file>
              <ns11:pathFileName>https://dev.ebpzh.ch/this/is/a/temporary/download/link/myFile.pdf</ns11:pathFileName>
              <ns11:mimeType>application/pdf</ns11:mimeType>
              <ns11:version>1.0.0</ns11:version>
            </ns11:file>
          </ns11:files>
          <ns11:comments>
            <ns10:comment ns10:lang="DE">Dokumentkommentar</ns10:comment>
          </ns11:comments>
          <ns11:keywords>
            <ns10:keyword ns10:lang="DE">Gesuchsunterlagen vom: dd.mm.yyyy</ns10:keyword>
          </ns11:keywords>
          <ns11:documentKind>Weitere Dokumente</ns11:documentKind>
        </ns2:document>
      </ns2:planningPermissionApplication>
      <ns2:relationshipToPerson>
        <ns2:role>applicant</ns2:role>
        <ns2:person>
          <ns3:identification>
            <ns3:personIdentification>
              <ns6:officialName>Heller</ns6:officialName>
              <ns6:firstName>Markus</ns6:firstName>
            </ns3:personIdentification>
          </ns3:identification>
          <ns3:address>
            <ns4:street>Bergstrasse</ns4:street>
            <ns4:houseNumber>234c</ns4:houseNumber>
            <ns4:town>Hausen</ns4:town>
            <ns4:swissZipCode>2223</ns4:swissZipCode>
          </ns3:address>
        </ns2:person>
      </ns2:relationshipToPerson>
      <ns2:relationshipToPerson>
        <ns2:role>project author</ns2:role>
        <ns2:person>
          <ns3:identification>
            <ns3:personIdentification>
              <ns6:officialName>Rost</ns6:officialName>
              <ns6:firstName>Philipp</ns6:firstName>
            </ns3:personIdentification>
          </ns3:identification>
          <ns3:address>
            <ns4:street>Untere Strasse</ns4:street>
            <ns4:houseNumber>43</ns4:houseNumber>
            <ns4:town>Bergen</ns4:town>
            <ns4:swissZipCode>5323</ns4:swissZipCode>
          </ns3:address>
        </ns2:person>
      </ns2:relationshipToPerson>
    </ns2:eventSubmitPlanningPermissionApplication>
  </ns2:delivery>
"""


class GetNextView(InstanceQuerysetMixin, RetrieveAPIView):
    queryset = Instance.objects

    def retrieve(self, request, **kwargs):
        response = HttpResponse(XML)
        response["Content-Type"] = "application/xml"
        return response
