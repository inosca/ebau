# Allgemeine Hinweise

- Der Typ `planningPermissionAplicationIdentifier` enthält unter `localId` unsere Dossiernummer ("Instance id")

- Der Type `localOrganisationId` enthält unter `organisationId` unsere Service id. Service ids können über den `/ech/v1/public-services/` endpoint abgefragt werden.

- Der von uns empfangene Typ `task`, um Stellungnahmen anzufordern (Spezifikation 3.2) muss zwingend die Service id der einzuladenden Stelle im `extension` Typ enthalten:

```xml
<ns2:extension>
  <serviceId>23</serviceId>
</ns2:extension>
```

- Der eCH-Standard forciert, dass bei den meisten Meldungen ein `document` mitgeschickt wird. Dieses `document` wird (mit Ausnahme von `accompanyingReport`) von eBau ignoriert.

- In einer `application` wird immer der Status `6701` gesetzt. Der korrekte Status aus dem eBau findet sich unter `namedMetaData.status`. Bei einer `statusNotification` wird immer der Status `in progress` gesetzt. Der korrekte Status findet sich im `remark`.

- `messageType` beinhaltet bei den von uns generierten Meldungen immer den Meldungstyp (`changeResponsibility`, `statusNotification`, etc). Bei empfangenen Meldungen wird das property ignoriert.
