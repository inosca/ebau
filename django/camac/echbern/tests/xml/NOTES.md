# Allgemeine Hinweise

- Der Typ `planningPermissionAplicationIdentifier` enthält unter `localId` unsere Dossiernummer ("Instance id")

- Der Type `localOrganisationId` enthält unter `organisationId` unsere Service id. Service ids können über den `/ech/v1/public-services/` endpoint abgefragt werden.

- Der von uns empfangene Typ `task`, um Stellungnahmen anzufordern (Spezifikation 3.2) muss zwingend die Service id der einzuladenden Stelle im `extension` Typ enthalten:

```xml
<ns2:extension>
  <serviceId>23</serviceId>
</ns2:extension>
```

- Der eCH-Standard forciert, dass in jeder meldung ein `document` mitgeschickt wird. In den meisten Fällen ignorieren wir das Dokument (Ausnahme: Accompanying Report)
