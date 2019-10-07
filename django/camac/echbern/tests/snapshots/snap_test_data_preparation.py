# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_get_document 1"] = {
    "ableitung-haeusliche-abwaesser": ["ARA", "Güllegrube"],
    "ableitung-in-guellegrube": "Nein",
    "abstellplaetze-fuer-fahrraeder-und-motorfahrraeder": 23,
    "aenderungen-dachflaechen-zufahrten-plaetzen": "Ja",
    "amts-verfugungsnummer": "555",
    "andere-dokument": ["Andere"],
    "anforderungen-eingehalten": [
        "Die Anforderungen sind gemäss Art. 11 – 15 BewD eingehalten."
    ],
    "anschluss-sammelkanaele-vorfluter-dokument": [
        "Zustimmung des Eigentümers für den Anschluss an die Sammelkanäle bzw. zur Einleitung in einen Vorfluter wenn die Gemeinde nicht Eigentümerin ist"
    ],
    "anzahl-abstellplaetze-fur-motorfahrzeuge": 23,
    "arbeit-waehrend-nachtzeit": "Ja",
    "art-der-baugrubenumschliessung": ["Spundwand"],
    "art-der-emmission-tabelle": [
        {
            "abluftentreinigungsanlage-beinhaltet": "Ja",
            "art-der-emmission": ["Gas- und dampfförmige Stoffe"],
            "brennstoff": "Holz",
            "feuerung": "Ja",
            "feuerwaermleistung-in-kw": 568,
            "kaminmuendung-ueberragt-dachfirst-um-meter": 89.0,
            "typ-der-abluftentreinigungsanlage": "Testabluftreinigungsanlage",
        }
    ],
    "art-der-fundationsmassnahmen": ["Tiefenfundation, Pfahlsystem"],
    "art-der-grundwasserabsenkung": ["Vakuumverfahren"],
    "atmosphaerischer-unterdruck": "Ja",
    "ausnahme-im-sinne-von-artikel-64-kenv": "Ja",
    "ausnahmegesuch-energie-dokument": ["Ausnahmegesuch Energie"],
    "ausnuetzung": "100",
    "ausnuetzung-dokument": ["Ausnützung"],
    "auto-oder-fahrradabstellplaetze": "Ja",
    "bau-im-wald-oder-innerhalb-von-30-m-abstand": "Ja",
    "baubeschrieb": ["Neubau"],
    "baugrunduntersuchung-dokument": [
        "Baugrunduntersuchung / Hydrogeologisches Gutachten"
    ],
    "baugruppe-bauinventar": "Ja",
    "baukosten-in-chf": 232323,
    "bauprofile-bleiben-bis-bauentscheid-stehen": [
        "Die Bauprofile sind gemäss Art. 16 BewD gestellt. Hiermit wird bestätigt, dass die Bauprofile bis zum rechtskräftigen Bauentscheid stehen bleiben und vor diesem Entscheid mit den Bauarbeiten nicht begonnen wird."
    ],
    "bauten-oder-pfaehlen-im-grundwasser": "Ja",
    "be-gid": "23",
    "beanspruchte-flache-ober-unterboden-2000-m2": "Ja",
    "beanspruchte-flaeche-ober-unterboden-5000-m2": "Ja",
    "begasung-moeglich": "Ja",
    "begruendung-waldabstand-unterschritten": "Testbegründung",
    "belasteter-standort": "Ja",
    "bemerkungen": "Testbemerkung",
    "berechnung-kinderspielplaetze-dokument": [
        "Berechnung Kinderspielplätze / Aufenthaltsbereiche"
    ],
    "berechnungen-abstellplaetze-dokument": ["Berechnungen Abstellplätze"],
    "beschreibung-bauvorhaben": "Testbeschreibung",
    "beschreibung-boden-untergrund": "Testanderebeschreibung",
    "beschreibung-der-prozessart-tabelle": [
        {
            "beschreibung-der-gefaehrdung": "Testbeschreibung",
            "hauptprozessart": "Rutschung",
            "prozessart": "Fliesslawine",
        }
    ],
    "beschreibung-geplante-taetigkeit": "Testtätigkeitsbeschreibung",
    "beschreibung-organismen": "Testanderebeschreibung",
    "beschreibung-tiefenfundation": "Testtiefenfundationsbeschreib",
    "besondere-brandrisiken": "Ja",
    "bestaetigung-hydrogeo-begleitung-dokument": [
        "Auftragsbestätigung des Fachbüro für die hydrogeologische Begleitung"
    ],
    "bestaetigung-liegenschaftsentwaesserung": [
        'Der/die Gesuchsteller/in bestätigt, dass die Liegenschaftsentwässerung gemäss dem AWA-Merkblatt "Entwässerung von Industrie- und Gewerbeliegenschaften" geplant und realisiert werden. Als Beilage enthält das Gesuch einen Umgebungsplan, auf dem bei allen Teilfächen die vorgesehene Nutzung, die Befestigungsart, das Gefälle sowie die Entwässerungsart eingetragen sind.'
    ],
    "bestaetigung-mit-unterschrift": [
        "Der/die Gesuchsteller/in resp. die bevollmächtigte Vertretung bestätigt mit rechtsgültiger Unterschrift, dass die elektronisch übermittelten Daten (inkl. dem unterzeichneten Situationsplan) vollständig und wahrheitsgetreu ausgefüllt und eingereicht worden sind."
    ],
    "betriebsweise": "Bivalent",
    "bezeichnung-baugruppe": "Testbaugruppe",
    "bisherige-nutzung": "Test bisherige Nutzung",
    "bodenschutzkonzept-dokument": ["Bodenschutzkonzept"],
    "brandschutzrisiken": [
        "Aussenwand: Bekleidung",
        "Tragwerk brennbar",
        "Dämmschichtbildende Systeme",
        "Brennbare Gase bis 1000 kg",
        "Brennbare Gase über 1000 kg",
        "bis 2000kg brennbare Flüssigkeit",
        "über 2000kg brennbare Flüssigkeit",
        "Pneulager bis 60t",
        "Pneulager über 60t",
        "Feuerwerkskörper bis 300kg",
        "Feuerwerkskörper über 300kg",
        "Mensch und Umwelt gefährdende Stoffe",
        "Explosionsgefährdete Räume oder Zonen",
        "Bauten mit Atrien oder Doppelfassaden",
        "Brandabschnittsfläche über 7200 m²",
        "Bruttogeschossfläche über 12000 m²",
        "Anwendung von Nachweisverfahren",
        "Hoher Anteil an Brandschutzmassnahmen",
        "Lagerung fester Brennstoffe 5m³",
    ],
    "brecher-oder-holzhacker": "Ja",
    "dach-farbe": "Testdachfarbe",
    "dach-form": "Testform",
    "dach-material": "Testdachmaterial",
    "dach-neigung": "Testneigung",
    "dauer-in-monaten": 23,
    "davon-in-garagen-oder-einstellhallen": 23,
    "davon-ueberdacht": 23,
    "dimensionierung-erdwaermesonden": "Berechnungsverfahren für komplexe Anlagen",
    "duschmoeglichkeit-in-der-schleuse": "Ja",
    "e-mail-energie": "test@example.com",
    "effektive-geschosszahl": 21,
    "eigenstaendiger-grossverbraucher": "Ja",
    "eigentuemer-tabelle": [
        {
            "grundbuch-nr-wald-eigentuemer": 23807,
            "name-wald-eigentuemer": "Testname",
            "nr-wald-eigentuemer": "23",
            "ort-wald-eigentuemer": "Burgdorf",
            "parzellen-nr": "56",
            "plz-wald-eigentuemer": 2323,
            "strasse-wald-eigentuemer": "Teststrasse",
            "vorname-wald-eigentuemer": "Testvorname",
            "waldabstand": 789,
        }
    ],
    "einhaltung-radonvorgaben": [
        "Der/die Gesuchsteller/in ist verantwortlich für die Einhaltung der Radonvorgaben gemäss Strahlenschutzverordnung des Bundes."
    ],
    "einreichen-button": ["Eingereicht"],
    "empfindlichkeitsstufe": "5",
    "energiedokumente-dokument": ["Energiedokumente"],
    "entsorgungskonzept-dokument": ["Entsorgungskonzept"],
    "entwaesserung-der-dachflaechen": "Neu",
    "entzug-von-waerme-mittels-erdwaermesonde": "Ja",
    "erhaltenswert": "Ja",
    "erleichterungen-waermeschutz": "Ja",
    "fabrikat": "Tesfabrikat",
    "fassaden-farbe": "Testfassadenfarbe",
    "fassaden-material": "Testfassadenmaterial",
    "fassadenplan-reklamestandort-dokument": [
        "Fassadenplan mit eingezeichnetem Reklamestandort"
    ],
    "feuerungsanlagen": ["Holzfeuerungen mit einer Feuerungswärmeleistung ≥ 70 kW"],
    "finden-bauarbeiten-in-der-nacht-statt": "Ja",
    "forstliche-baute": "Ja",
    "fruchtfolgeflaeche-ausgeschieden": "Ja",
    "fuellmenge-in-kg": 555,
    "fuellmenge-total-in-liter": 9000,
    "fundation-system": "Testsystem",
    "gebaeudeversicherungswert-in-chf": 90000,
    "gebiet-mit-archaeologischen-objekten": "Ja",
    "gebiet-mit-naturgefahren": "Ja",
    "gefaehrlich-fuer-bevoelkerung-oder-umwelt": "Ja",
    "gefahrengutachten-dokument": ["Gefahrengutachten"],
    "gefahrenstufe": ["Rot"],
    "gemeinde": "Burgdorf",
    "gentechnisch-veraenderte-organismen": "Ja",
    "gentechnisch-veraenderte-pathogene-organismen": "Ja",
    "geplante-anlagen": ["Solar- oder Photovoltaik-Anlage"],
    "geplanter-baustart": "2019-09-15",
    "geschossflaeche-in-quadratmeter": "200",
    "geschossflaechen-dokument": ["Geschossflächen"],
    "gesuch-ausnahmebewilligung-dokument": [
        "Gesuch für eine Ausnahmebewilligung mit hydrogeologisches Gutachten und Nachweis, dass die Durchflusskapazität des Grundwassers gegenüber dem unbeinflussten Zustand um höchstens 10% vemindert wird."
    ],
    "gesuch-erleichterung-waermeschutz-dokument": [
        "Gesuch um Erleichterung oder Befreiung Wärmeschutz"
    ],
    "gesuch-zur-ausnahme-dokument": ["Gesuch zur Ausnahme gemäss Art 31 Abs. 2 LSV"],
    "gewaesserschutzbereich": ["Ao"],
    "gibt-es-bewilligungspflichtige-reklame": "Ja",
    "grenzwerte-fenster-ueberschritten": "Ja",
    "grenzwerte-ueberschritten": "Ja",
    "gruenflache-in-quadratmeter": "23",
    "gruenflaeche-dokument": ["Grünfläche"],
    "grundriss-angabe-bodenflaeche-dokument": [
        "Grundriss (Massstäblich (1:100 / 1:50) mit Angabe der Bodenfläche)"
    ],
    "grundriss-dokument": ["Grundriss"],
    "grundstuecksentwaesserungsplan-dokument": [
        "Grundstücksentwässerungsplan SN 592 000"
    ],
    "grundwasserschutzzonen": ["S1"],
    "gueterumschlag-im-freien-oder-an-rampen": "Ja",
    "gwr-egid": "23",
    "handelt-es-sich-um-ein-baudenkmal": "Ja",
    "handelt-es-sich-um-ein-sensibles-objekt": "Ja",
    "handelt-es-sich-um-eine-baute-im-wald": "Ja",
    "heizleistungsbedarf-boden-untergrund": 555,
    "hepa-filter-abluft": "Nein",
    "hepa-filter-zuluft": "Nein",
    "hoechstmoeglicher-grundwasserspiegel": "23",
    "hoehe": ["Mittlere Höhe zwischen 11 m und 30 m"],
    "hoehe-groesser-als-1800-m-ue-m": "Ja",
    "hydrogeologische-begleitung-dokument": [
        "Auftragsbestätigung für Hydrogeologische Begleitung"
    ],
    "im-grundwasser-verbleibendes-einbauvolumen": 7,
    "integration-anderer-gebaeude": "Ja",
    "ist-das-vorhaben-energierelevant": "Ja",
    "ist-durch-das-bauvorhaben-boden-betroffen": "Ja",
    "ist-fuer-das-vorhaben-eine-rodung-notwendig": "Ja",
    "ist-mit-bauabfaellen-zu-rechnen": "Ja",
    "k-objekt": "Ja",
    "kaelteleistung-boden-untergrund": 2323,
    "kaeltemittel": "Testkältemittel",
    "kanalisationskatasterplan-dokument": ["Kanalisationskatasterplan"],
    "kann-inhalt-zurueckgehalten-werden": "Nein",
    "keine-rueckhiebe-oder-aushiebe": [
        "Die Bauherrschaft nimmt für sich und ihre Rechtsnachfolge zur Kenntnis, dass keine Rückhiebe oder andere über das Kapprecht hinausgehenden Aushiebe an dem vom Näherbau tangierten Wald bewilligt werden; es ist verboten, auch wenn der Wald ihr gehört, solche Hiebe zwecks Verminderung des Schattenwurfes, zur Verbesserung der Aussicht oder aus anderen Gründen vorzunehmen."
    ],
    "keine-tangierung-natur-wild-vogelschutz": [
        "Der/die Gesuchsteller/in bestätigt, dass er keinen Tatbestand zu den Bestimmungen zum Natur-, Wild- und Vogelschutz tangiert."
    ],
    "klassierung-der-taetigkeit": "Klasse 2",
    "kontaktperson-name-energie": "Testkontaktvorname",
    "kontaktperson-vorname-energie": "Testkontaktname",
    "kurzbericht-datum": "2019-10-19",
    "kurzbericht-gemaess-stfv-dokument": ["Kurzbericht gemäss StFV"],
    "laermige-bauphase-laenger-als-6-tage": "Ja",
    "laermintensive-bauarbeiten-ueber-6-tage": "Ja",
    "leitungsbau-auf-landwirtschaftlichem-boden": "Ja",
    "liegt-die-baute-im-waldabstandsbereich": "Ja",
    "liegt-kurzbericht-vor": "Ja",
    "liegt-risikoermittlung-vor": "Ja",
    "maschinen-mit-aussenlaermimmissionen": "Ja",
    "mehr-als-1500-m3-bodenmaterial": "Ja",
    "mehr-als-500-m3-bodenmaterial": "Ja",
    "meldeblatt-terrainveraenderungen-dokument": [
        "Meldeblatt für Terrainveränderungen zur Bodenaufwertung"
    ],
    "meldeblatt-zur-fruchtfolgeflaeche-dokument": ["Meldeblatt zur Fruchtfolgefläche"],
    "menge-des-abzuleitenden-grundwassers": 9000,
    "mengenschwelle-hochaktive-stoffe": "Ja",
    "mengenschwelle-sonderabfaelle-ueberschritten": "Ja",
    "mit-invasiven-neophyten-belasteter-boden": "Ja",
    "mit-schadstoffen-belastete-luft-aus-gebaeuden": "Ja",
    "mittlerer-grundwasserspiegel": "12",
    "nachweis-anforderungen-dokument": ["Nachweis Anforderungen gemäss Art 31 LSV"],
    "name-betrieb-energie": "Testbetrieb",
    "name-des-gewaessers-regen": "Mittelmeer",
    "naturschutz": "Ja",
    "neubau-abwasseranlagen-grundleitungen": "Ja",
    "neue-dachflaechen-in-quadratmeter": 23.0,
    "nicht-forstliche-kleinbaute": "Nein",
    "nr": "23",
    "nummer-energie": "5",
    "nutzungsart": ["Wohnen"],
    "nutzungszone": "Testnutzungszone",
    "oberflaechengewaesser-regenabwasserleitung": "Ja",
    "objekt-des-besonderen-landschaftsschutzes": "Ja",
    "objektbezeichnung": "Testobjektbezeichnung",
    "organismen-in-anlage": [
        "Prionen",
        "Viren",
        "Bakterien",
        "Parasiten",
        "Pflanzen",
        "andere",
    ],
    "ort-energie": "Burgdorf",
    "ort-grundstueck": "Burgdorf",
    "parzelle": [
        {
            "baurecht-nummer": "23",
            "e-grid-nr": "23",
            "lagekoordinaten-nord": "2",
            "lagekoordinaten-ost": "1",
            "liegenschaftsnummer": 23,
            "nummer-parzelle": "23",
            "ort-parzelle": "Burgdorf",
            "parzellennummer": "1586",
            "plz-parzelle": 2323,
            "strasse-parzelle": "Teststrasse",
        }
    ],
    "personalien-gesuchstellerin": [
        {
            "e-mail-gesuchstellerin": "test@example.com",
            "juristische-person-gesuchstellerin": "Nein",
            "name-gesuchstellerin": "Testname",
            "nummer-gesuchstellerin": "23",
            "ort-gesuchstellerin": "Burgdorf",
            "plz-gesuchstellerin": 2323,
            "strasse-gesuchstellerin": "Teststrasse",
            "telefon-oder-mobile-gesuchstellerin": "0781234567",
            "vorname-gesuchstellerin": "Testvorname",
        }
    ],
    "personalien-vertreterin-mit-vollmacht": [
        {
            "e-mail-vertreterin": "test@example.com",
            "juristische-person-vertreterin": "Nein",
            "name-vertreterin": "Testname",
            "nummer-vertreterin": "23",
            "ort-vertreterin": "Burgdorf",
            "plz-vertreterin": 2323,
            "strasse-vertreterin": "Teststrasse",
            "telefon-oder-mobile-vertreterin": "0791234567",
            "vollmacht": [
                "Der/die Gesuchsteller/in bestätigt mit Unterschrift, die Generalvollmacht an Bevollmächtigte"
            ],
            "vorname-vertreterin": "Testvorname",
        }
    ],
    "plaene-gewaesserschutz-dokument": [
        "Pfahl-, Injektions- oder Ankerpläne, Situation und Schnittpläne mit Koten in m ü.M. (falls geplant)"
    ],
    "plaene-schleusen-dokument": ["Pläne - Zugang zum Arbeitsbereich über Schleusen"],
    "plaene-unterdruck-dokument": ["Pläne - Atmosphärischer Unterdruck"],
    "platz-und-verkehrsflaechen": "Neu",
    "plz-energie": 2000,
    "projektverfasserin-identisch": "Nein",
    "qss-stufe": ["1"],
    "rechtliche-sicherung-fremden-bodens": "Nein",
    "regeneration-oder-aktive-thermische-aufladung": "Ja",
    "regierungsratsbeschluss-bauinventar-dokument": [
        "Regierungsratsbeschluss zum Bauinventar"
    ],
    "reklame-tabelle": [
        {
            "abschaltung-geplant": "Nein",
            "abstand-boden-bis-unterkante": 6,
            "abstand-fahrbahnrand-bis-aussenkante": 9,
            "abstand-fassade-bis-aussenkante": 7,
            "art-der-beleuchtung": [
                "Keine",
                "Leuchtkasten",
                "einzelne Buchstaben",
                "blinkend",
                "Bildschirm",
                "von oben",
                "von unten",
            ],
            "bemerkung-zur-beleuchtung": "Testbemerkung",
            "bemerkungen-reklame": "Testbemerkung",
            "breite-in-cm": "90000",
            "gesamtlaenge-in-cm": 90000.0,
            "grundfarben": "schwarz",
            "montageort-am-gebaeude": "Testmontageort",
            "montageort-freistehende-reklame": "Testbeschrieb",
            "reklame-neu-oder-ersatz": "Neu",
            "schriftfarben-bei-nacht": "blau",
            "schriftfarben-bei-tag": "rot",
            "text": "Testtext",
        }
    ],
    "risikoermittlung-datum": "2019-10-26",
    "risikoermittlung-gemaess-stfv-dokument": ["Risikoermittlung gemäss StFV"],
    "rodungs-und-ersatzaufforstungsplan-dokument": [
        "Rodungs- und Ersatzaufforstungsplan"
    ],
    "rodungsgesuchsformular-bafu-dokument": ["Rodungsgesuchsformular BAFU"],
    "rrb": "Ja",
    "rrb-vom": "2019-10-26",
    "rueckbau-checkliste-selbstdeklaration-dokument": [
        "Rückbau Checkliste / Selbstdeklaration"
    ],
    "sammelschutzraum": "Nein",
    "sanitaertechnische-anpassungen-liegenschaft": "Ja",
    "schmutz-oder-mischwasserkanalisation": "Ja",
    "schnitt-dokument": ["Schnitt"],
    "schnittplan-gewaesserschutz-dokument": [
        "Schnittplan mit Untergeschoss und Baugrubenumschliessung, eingezeichneter Wasserhaltung sowie mittlerem Grundwasserspiegel (mit den entsprechenden Koten in m ü.M.)"
    ],
    "schuetzenswert": "Ja",
    "schutzraum-pflicht": "Ja",
    "schutzraumbefreiung-beantragt": "Nein",
    "seit-welchem-jahr-besteht-der-betrieb-am-standort": 1900,
    "sicherheitsdaten-stoerfallvorsorge-dokument": [
        "Sicherheitsdatenblätter Störfallvorsorge"
    ],
    "sicherheitsmassnahmen-eingehalten": "Ja",
    "sicherheitsstufe-der-anlage": "Stufe 4",
    "sicherungsleistung-befreit-dokument": [
        "Vertrag - mit Sicherungsleistung befreite Gebäude"
    ],
    "sicherungsmassnahme-dokument": ["Sicherungsmassnahme"],
    "sind-bauschadstoffe-zu-erwarten": "Ja",
    "sind-belange-des-gewasserschutzes-betroffen": "Ja",
    "situationsplan-dokument": ["Situationsplan"],
    "skizze-der-reklame-mit-farbangaben-dokument": [
        "Skizze der Reklame mit Farbangaben"
    ],
    "sondenmodelle": [
        {
            "anzahl-sonden": 6,
            "bohrlaenge-einzeln-in-meter": 466,
            "sondendurchmesser-in-mm": 23,
            "sondenmodell": "Doppel-U-Sonde",
        }
    ],
    "spezifische-waermeentzugsleistung-in-wm": "453",
    "sterilisation-abwasser-dokument": ["Sterilisation Abwasser"],
    "sterilisation-des-abwassers": "Ja",
    "stoerende-lichtreflektionen": "Ja",
    "stoffliste-stoerfallvorsorge-dokument": ["Stoffliste Störfallvorsorge"],
    "strasse-energie": "Teststrasse",
    "strasse-flurname": "Teststrasse",
    "system": "Testsystem",
    "telefon-oder-mobile-energie": "0791234567",
    "terrain-kote": "100",
    "terrainveraenderung-weniger-als-2000m2": "Ja",
    "tiefste-kote-der-aushubsohle": 500.0,
    "total-bohrlaenge": "666",
    "tragkonstruktion-decken": "Testdecken",
    "tragkonstruktion-stuetzen": "Teststützen",
    "tragkonstruktion-waende": "Testände",
    "typ-dachflaechen": "Typ A",
    "typ-platz-und-verkehrsflaechen": "Über Schulter",
    "typ-waermepumpen": "Testtyp",
    "ueberbauung-dokument": ["Überbauung"],
    "ueberbauung-in-prozent": "100",
    "ueberbauungsordnung": "???",
    "uebersichtsplan-dokument": ["Übersichtsplan 1:25'000"],
    "um-was-fuer-ein-gebaeude-handelt-es-sich": ["EFH"],
    "umfasst-die-bauabfallmenge-200-kubikmeter": "Ja",
    "unterkante-der-baugrubenumschliessung": 200.0,
    "verfahren-fuer-die-sterilisation-des-abwassers": "Testverfahren",
    "verpflichtung-bei-handaenderung": [
        "Bei einer allfälligen Handänderung verpflichten sich die Bauherrschaft und Grundeigentümerin/Grundeigentümer, bzw. Baurechtsnehmerin/Baurechtsnehmer, diese Erklärung einer allfälligen Rechtsnachfolge zu überbinden."
    ],
    "versickerung": "Ja",
    "versickerung-dachflaechen": "Ja",
    "versickerung-platz-und-verkehrsflaechen": "Ja",
    "versickerungsanlagen-dokument": [
        "Pläne, Berichte und Berechnungen über neue und bestehende Versickerungsanlagen"
    ],
    "vertrag": "Ja",
    "vertrag-vom": "2019-10-19",
    "vertrag-zum-bauinventar-dokument": ["Vertrag zum Bauinventar"],
    "verwendungszweck-boden-untergrund": ["Raumheizung", "Kühlen", "Andere"],
    "verwendungszweck-der-anlage": [
        "Forschung",
        "Produktion",
        "Diagnostik",
        "Tieranlage",
    ],
    "verwertung-abgetragenem-boden-dokument": [
        "Deklaration zur Verwertung von abgetragenem Boden"
    ],
    "verzicht-schadensersatz-naturereignisse": [
        "Der/die Gesuchsteller/in verzichtet für sich und seine/ihre Rechtsnachfolger ausdrücklich auf jeden Ersatz von Schaden, der durch den Forstbetrieb oder durch Naturereignisse, wie Schneedruck, Windfall usw. an der zu erstellenden Baute, bzw. ähnlichen Anlage verursacht werden könnte. Vorbehalten bleiben jedoch die Bestimmungen der Art. 41 ff. OR."
    ],
    "vollmacht-dokument": ["Vollmacht"],
    "vorabklaerung-dokument": ["Vorabklärung"],
    "vorbereitende-massnahmen": ["Rammen"],
    "waermetraegerfluessigkeit": "Methylalkohol (Methanol)",
    "weitere-personen": ["Vertreter/in mit Vollmacht"],
    "welche-waermepumpen": ["Boden / Untergrund"],
    "werden-bestehende-bauten-zurueckgebaut": "Ja",
    "werden-brandschutzabstaende-unterschritten": "Ja",
    "werden-luftemissionen-erzeugt": "Ja",
    "wildtierschutz": "Ja",
    "wird-aussenlaerm-erzeugt": "Ja",
    "wohnungen": [
        {
            "anzahl-wohnungen-bestehend": 0,
            "anzahl-wohnungen-neu": 21,
            "wohnungsgroesse": "7",
        }
    ],
    "wurden-vorabklaerungen-durchgefuehrt": "Nein",
    "zufahrten-plaetze-in-quadratmeter": 23.0,
    "zugang-zum-arbeitsbereich-ueber-schleuse": "Ja",
    "zulaessige-geschosszahl": "23",
    "zustimmung-der-anstoesser-dokument": [
        "Zustimmung der Anstösser falls die Versickerung nicht publiziert wurde"
    ],
}
