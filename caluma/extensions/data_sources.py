from caluma.data_source.data_sources import BaseDataSource
from caluma.data_source.utils import data_source_cache


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    # TODO: Make a request to get the municipalities

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        return [
            ["20011", "Oberburg"],
            ["20013", "Rüderswil"],
            ["20017", "Trubschachen"],
            ["20019", "Wynigen"],
            ["2", "Burgdorf"],
            ["20003", "Eggiwil"],
            ["20005", "Hasle b. B."],
            ["20007", "Langnau i. E."],
            ["20009", "Lyssach"],
            ["20015", "Utzenstorf"],
        ]


class Services(BaseDataSource):
    info = "List of services from Camac"

    # TODO: Make a request to get the services

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        data = [
            [
                "20031",
                "Amt für Bevölkerungsschutz, Sport und Militär- Abteilung Zivil- und Bevölkerungsschutz",
            ],
            ["20032", "Amt für Gemeinden und Raumordnung - AbteilungBauen"],
            ["20034", "Amt für Gemeinden und Raumordnung - AbteilungKantonsplanung"],
            [
                "20036",
                "Amt für Gemeinden und Raumordnung - AbteilungOrts- und Regionalplanung",
            ],
            [
                "20038",
                "Amt für Gemeinden und Raumordnung - FachstelleSchiesslärm, Militärfluglärm, Lärm von militärischen Anlagen",
            ],
            ["20039", "Amt für Grundstücke und Gebäude"],
            ["20040", "Amt für Kindergarten, Volksschule und Beratung(AKVB)"],
            ["20042", "Amt für Kultur - Archäologischer Dienst desKantons Bern"],
            ["20043", "Amt für Kultur - Denkmalpflege des KantonsBern"],
            ["20045", "Amt für öffentlichen Verkehr undVerkehrskoordination"],
            ["20046", "Amt für Umweltkoordination und Energie -Energie"],
            [
                "20047",
                "Amt für Umweltkoordination und Energie -Umwelt und Nachhaltige Entwicklung (UNE)",
            ],
            ["20048", "Amt für Wald KAWA - Abteilung Fachdienste undRessourcen"],
            ["20049", "Amt für Wald KAWA - AbteilungNaturgefahren"],
            [
                "20050",
                "Amt für Wasser und Abfall des Kantons Bern -Betriebe und Abfall",
            ],
            [
                "20051",
                "Amt für Wasser und Abfall des Kantons Bern -Gewässerregulierung",
            ],
            [
                "20052",
                "Amt für Wasser und Abfall des Kantons Bern-Siedlungswasserwirtschaft",
            ],
            ["20053", "Amt für Wasser und Abfall des Kantons Bern -Wassernutzung"],
            ["3", "Baukontrolle Burgdorf"],
            ["20004", "Baukontrolle Eggiwil"],
            ["20006", "Baukontrolle Hasle b. B."],
            ["20008", "Baukontrolle Langnau"],
            ["20010", "Baukontrolle Lyssach"],
            ["20012", "Baukontrolle Oberburg"],
            ["20014", "Baukontrolle Rüderswil"],
            ["20018", "Baukontrolle Trubschachen"],
            ["20016", "Baukontrolle Utzenstorf"],
            ["20020", "Baukontrolle Wynigen"],
            ["20054", "beco Berner Wirtschaft - Immissionsschutz"],
            [
                "20055",
                "beco Berner Wirtschaft - Sicherheit undGesundheit am Arbeitsplatz",
            ],
            ["20056", "beco Economie bernoise - Sécurité &amp; santéau travail"],
            ["20229", "BKW (Regierungsstatthalteramt Emmental)"],
            [
                "20059",
                "Commission cantonale pour la protection dessites et du paysage (CPS)",
            ],
            ["20068", "Fachstelle Hindernisfreies Bauen"],
            ["20057", "Gebäudeversicherung Bern (GVB)"],
            [
                "20058",
                "Kant. Kommission zur Pflege der Orts- undLandschaftsbilder (OLK)",
            ],
            ["20060", "Kantonales Laboratorium"],
            ["20061", "Kantonsarztamt"],
            ["20062", "Kantonspolizei Bern - Fachstelle Lärmakustik /Lasertechnik"],
            [
                "20066",
                "LANAT Amt für Landwirtschaft und Natur -Abteilung Strukturverbesserungen und Produktion (ASP)",
            ],
            [
                "20063",
                "LANAT Amt für Landwirtschaft und Natur  -Fischereiinspektorat (FI)",
            ],
            ["20064", "LANAT Amt für Landwirtschaft und Natur -Jagdinspektorat (JI)"],
            ["20065", "LANAT Amt für Landwirtschaft und Natur -Naturförderung (ANF)"],
            ["20067", "LANAT Amt für Landwirtschaft und Natur -Veterinärdienst (VeD)"],
            ["2", "Leitbehörde Burgdorf"],
            ["20003", "Leitbehörde Eggiwil"],
            ["20005", "Leitbehörde Hasle b. B."],
            ["20007", "Leitbehörde Langnau"],
            ["20009", "Leitbehörde Lyssach"],
            ["20011", "Leitbehörde Oberburg"],
            ["20013", "Leitbehörde Rüderswil"],
            ["20017", "Leitbehörde Trubschachen"],
            ["20015", "Leitbehörde Utzenstorf"],
            ["20019", "Leitbehörde Wynigen"],
            [
                "20044",
                "Office de la Culture  - Service des monumentshistoriques du canton de Berne",
            ],
            [
                "20041",
                "Office de l'enseignement préscolaire etobligatoire, du conseil et de l'orientation (OECO)",
            ],
            ["20069", "Procap - Région Bienne / Jura bernois - PierreA. Chanez"],
            ["20021", "Regierungsstatthalteramt Bern-Mittelland"],
            ["20022", "Regierungsstatthalteramt Biel/Bienne"],
            ["20023", "Regierungsstatthalteramt Emmental"],
            ["20024", "RegierungsstatthalteramtFrutigen-Niedersimmental"],
            ["20025", "RegierungsstatthalteramtInterlaken-Oberhasli"],
            ["20026", "Regierungsstatthalteramt Jura bernois"],
            ["20027", "Regierungsstatthalteramt Oberaargau"],
            ["20028", "RegierungsstatthalteramtObersimmental-Saanen"],
            ["20029", "Regierungsstatthalteramt Seeland"],
            ["20030", "Regierungsstatthalteramt Thun"],
            [
                "20070",
                "Strassenverkehrs- und Schifffahrtsamt SVSA -Abteilung Schifffahrt",
            ],
            [
                "20071",
                "Strassenverkehrs- und Schifffahrtsamt SVSA -Sonderbewilligungen",
            ],
            ["20228", "Testfachstelle (Burgdorf)"],
            ["20073", "Tiefbauamt des Kantons Bern - AbteilungNationalstrassen Bau"],
            [
                "20072",
                "Tiefbauamt des Kantons Bern -  AbteilungNationalstrassen Betrieb",
            ],
            ["20074", "Tiefbauamt des Kantons Bern - FachstelleLärmschutz"],
            [
                "20076",
                "Tiefbauamt des Kantons Bern -Oberingenieurkreis II - Bern Mittelland",
            ],
            [
                "20077",
                "Tiefbauamt des Kantons Bern - Oberingenieurkreis III - Seeland / Berner Jura",
            ],
            ["20075", "Tiefbauamt des Kantons Bern - Oberingenieurkreis I - Oberland"],
            [
                "20078",
                "Tiefbauamt des Kantons Bern -Oberingenieurkreis IV - Oberaargau / Emmental",
            ],
            [
                "20035",
                "Unité francophone de l'OACOT – Service del'aménagement cantonal",
            ],
            [
                "20037",
                "Unité francophone de l'OACOT - Service del'aménagement local et régional",
            ],
            ["20033", "Unité francophone de l'OACOT - Service desconstructions"],
            [
                "20199",
                "Unterfachstelle AGR – Amt für Kultur -Denkmalpflege des Kantons Bern",
            ],
            [
                "20079",
                "Unterfachstelle Amt für Bevölkerungsschutz,Sport und Militär - Abteilung Zivil- und Bevölkerungsschutz",
            ],
            [
                "20080",
                "Unterfachstelle Amt für Gemeinden undRaumordnung - Abteilung Bauen",
            ],
            [
                "20082",
                "Unterfachstelle Amt für Gemeinden undRaumordnung - Abteilung Kantonsplanung",
            ],
            [
                "20084",
                "Unterfachstelle Amt für Gemeinden undRaumordnung - Abteilung Orts- und Regionalplanung",
            ],
            [
                "20086",
                "Unterfachstelle Amt für Gemeinden undRaumordnung - Fachstelle Schiesslärm, Militärfluglärm, Lärm vonmilitärischen Anlagen",
            ],
            ["20087", "Unterfachstelle Amt für Grundstücke undGebäude"],
            [
                "20088",
                "Unterfachstelle Amt für Kindergarten,Volksschule und Beratung (AKVB)",
            ],
            [
                "20090",
                "Unterfachstelle Amt für Kultur -Archäologischer Dienst des Kantons Bern",
            ],
            ["20091", "Unterfachstelle Amt für Kultur - Denkmalpflegedes Kantons Bern"],
            [
                "20093",
                "Unterfachstelle Amt für öffentlichen Verkehrund Verkehrskoordination",
            ],
            [
                "20094",
                "Unterfachstelle Amt für Umweltkoordination undEnergie - Energie",
            ],
            [
                "20095",
                "Unterfachstelle Amt für Umweltkoordination undEnergie - Umwelt und Nachhaltige Entwicklung (UNE)",
            ],
            [
                "20096",
                "Unterfachstelle Amt für Wald KAWA - AbteilungFachdienste und Ressourcen",
            ],
            ["20097", "Unterfachstelle Amt für Wald KAWA - AbteilungNaturgefahren"],
            [
                "20098",
                "Unterfachstelle Amt für Wasser und Abfall desKantons Bern - Betriebe und Abfall",
            ],
            [
                "20099",
                "Unterfachstelle Amt für Wasser und Abfall desKantons Bern - Gewässerregulierung",
            ],
            [
                "20100",
                "Unterfachstelle Amt für Wasser und Abfall desKantons Bern -Siedlungswasserwirtschaft",
            ],
            [
                "20101",
                "Unterfachstelle Amt für Wasser und Abfall desKantons Bern - Wassernutzung",
            ],
            ["20185", "Unterfachstelle Anschluss Elektrizität"],
            ["20188", "Unterfachstelle Anschluss Fernmeldenetz"],
            ["20186", "Unterfachstelle Anschluss Gas"],
            ["20187", "Unterfachstelle AnschlussGemeinschaftsantenne"],
            ["20184", "Unterfachstelle Anschluss Wasser"],
            ["20173", "Unterfachstelle ARA mittleres Emmental"],
            [
                "20153",
                "Unterfachstelle Bauverwaltung (Benützung vonöffentlichem Terrain)",
            ],
            ["20150", "Unterfachstelle Bauverwaltung Langnau(Gewässerschutz Gemeinde)"],
            [
                "20151",
                "Unterfachstelle Bauverwaltung Langnau(Gewässerschutz Kanton - Mitbericht)",
            ],
            ["20152", "Unterfachstelle Bauverwaltung Langnau(Strassenbaupolizei)"],
            ["20102", "Unterfachstelle beco Berner Wirtschaft -Immissionsschutz"],
            [
                "20103",
                "Unterfachstelle beco Berner Wirtschaft -Sicherheit und Gesundheit am Arbeitsplatz",
            ],
            [
                "20104",
                "Unterfachstelle beco Economie bernoise -Sécurité &amp; santé au travail",
            ],
            ["20201", "Unterfachstelle Berner Heimatschutz(Burgdorf)"],
            ["20204", "Unterfachstelle Berner Heimatschutz(Langnau)"],
            ["20142", "Unterfachstelle Berner Heimatschutz(Lyssach)"],
            ["20218", "Unterfachstelle BKW Energie AG (Eggiwil)"],
            ["20223", "Unterfachstelle BKW Energie AG (Hasle b.B.)"],
            ["20202", "Unterfachstelle BKW Energie AG (Langnau)"],
            ["20208", "Unterfachstelle BKW Energie AG(Rüderswil)"],
            ["20157", "Unterfachstelle BKW Energie AG(Trubschachen)"],
            ["20137", "Unterfachstelle BLS AG"],
            ["20219", "Unterfachstelle BLS Netz AG"],
            ["20167", "Unterfachstelle Brandschutz"],
            ["20134", "Unterfachstelle Brandschutzexperten"],
            ["20193", "Unterfachstelle Brunnenmeister"],
            ["20179", "Unterfachstelle Brunnenmeister MartinSchifferli"],
            [
                "20107",
                "Unterfachstelle Commission cantonale pour laprotection des sites et du paysage (CPS)",
            ],
            [
                "20155",
                "Unterfachstelle EBL (Genossenschaft ElektraBaselland) (Gemeinschaftsantenne)",
            ],
            ["20224", "Unterfachstelle EBL Telecom Media AG"],
            ["20207", "Unterfachstelle EBL Telecom Media AG(Rüderswil)"],
            ["20176", "Unterfachstelle EBL Telecom Media AG(Trubschachen)"],
            ["20138", "Unterfachstelle eicher + pauli Bern AG"],
            ["20177", "Unterfachstelle Elektra Rüderswil"],
            ["20178", "Unterfachstelle Elektra Schwanden"],
            ["20164", "Unterfachstelle Emmental Trinkwasser"],
            ["20196", "Unterfachstelle Energieberater"],
            ["20172", "Unterfachstelle Energieberatung Stefan SchwarzAG"],
            ["20162", "Unterfachstelle Energiefachmann"],
            ["20190", "Unterfachstelle Energiekontrolleur"],
            ["20214", "Unterfachstelle Energienachweis"],
            [
                "20221",
                "Unterfachstelle EnergietechnischerMassnahmennachweis (Hasle b. B.)",
            ],
            [
                "20183",
                "Unterfachstelle EnergietechnischerMassnahmennachweis (Utzenstorf)",
            ],
            ["20170", "Unterfachstelle Energie- und WasserversorgungOberburg"],
            ["20220", "Unterfachstelle Feueraufseher Hasle b. B."],
            ["20205", "Unterfachstelle Feueraufseher Lyssach"],
            ["20206", "Unterfachstelle Feueraufseher Rüderswil"],
            ["20210", "Unterfachstelle FeueraufseherTrubschachen"],
            ["20209", "Unterfachstelle Feueraufseher Utzenstorf"],
            ["20159", "Unterfachstelle Feueraufseher Wynigen"],
            ["20160", "Unterfachstelle Feuerwehr Lyssach"],
            ["20139", "Unterfachstelle Feuerwehr und Zivilschutz"],
            ["20105", "Unterfachstelle Gebäudeversicherung Bern(GVB)"],
            ["20226", "Unterfachstelle Gemeindeingenieur"],
            ["20163", "Unterfachstelle Genossenschaft ElektraJegenstorf"],
            ["20182", "Unterfachstelle Gewässerschutzbewilligung"],
            ["20147", "Unterfachstelle GLB Emmental (PrüfstelleENM)"],
            ["20215", "Unterfachstelle GLB, Energienachweis"],
            ["20165", "Unterfachstelle Grunder Ingenieure AG"],
            ["20189", "Unterfachstelle Heimatschutz"],
            ["20145", "Unterfachstelle Kaminfeger Hiltbrunner GmbH(Feueraufseher)"],
            ["20213", "Unterfachstelle Kaminfeger Joost AG"],
            ["20191", "Unterfachstelle Kanalisationskontrolleur"],
            [
                "20106",
                "Unterfachstelle Kant. Kommission zur Pflegeder Orts- und Landschaftsbilder (OLK)",
            ],
            ["20108", "Unterfachstelle Kantonales Laboratorium"],
            ["20109", "Unterfachstelle Kantonsarztamt"],
            [
                "20110",
                "Unterfachstelle Kantonspolizei Bern -Fachstelle Lärmakustik / Lasertechnik",
            ],
            [
                "20198",
                "Unterfachstelle LANAT - AbteilungStrukturverbesserungen und Produktion (ASP)",
            ],
            [
                "20114",
                "Unterfachstelle LANAT Amt für Landwirtschaftund Natur - Abteilung Strukturverbesserungen und Produktion (ASP)",
            ],
            [
                "20111",
                "Unterfachstelle LANAT Amt für Landwirtschaftund Natur  - Fischereiinspektorat (FI)",
            ],
            [
                "20112",
                "Unterfachstelle LANAT Amt für Landwirtschaftund Natur - Jagdinspektorat (JI)",
            ],
            [
                "20113",
                "Unterfachstelle LANAT Amt für Landwirtschaftund Natur - Naturförderung (ANF)",
            ],
            [
                "20115",
                "Unterfachstelle LANAT Amt für Landwirtschaftund Natur  -Veterinärdienst (VeD)",
            ],
            ["20192", "Unterfachstelle Liegenschaftskommission"],
            ["20197", "Unterfachstelle Localnet"],
            ["20200", "Unterfachstelle Localnet AG (Burgdorf)"],
            ["20141", "Unterfachstelle Localnet AG (Lyssach)"],
            ["20212", "Unterfachstelle Localnet AG (Wynigen)"],
            ["20225", "Unterfachstelle Nachführungsgeometer"],
            ["20149", "Unterfachstelle Öffentliche Sicherheit Langnau(Feuerwehr)"],
            ["20148", "Unterfachstelle Öffentliche Sicherheit Langnau(Gastgewerbe)"],
            [
                "20092",
                "Unterfachstelle Office de la Culture  -Service des monuments historiques du canton de Berne",
            ],
            [
                "20089",
                "Unterfachstelle Office de l'enseignementpréscolaire et obligatoire, du conseil et de l'orientation (OECO)",
            ],
            ["20195", "Unterfachstelle onyx"],
            ["20140", "Unterfachstelle Ordnung und Sicherheit"],
            ["20169", "Unterfachstelle Ostag Energieberatung"],
            ["20168", "Unterfachstelle Ostag Gewässerschutz"],
            ["20161", "Unterfachstelle OSTAG Ingenieure AG"],
            ["20116", "Unterfachstelle Procap - FachstelleHindernisfreies Bauen"],
            [
                "20117",
                "Unterfachstelle Procap - Région Bienne / Jurabernois - Pierre A. Chanez",
            ],
            ["20175", "Unterfachstelle Ruefer Ingenieure AG"],
            ["20203", "Unterfachstelle SBB AG (Langnau)"],
            ["20158", "Unterfachstelle SBB AG (Lyssach)"],
            ["20227", "Unterfachstelle Schwellenkoorporation"],
            ["20146", "Unterfachstelle Stefan Schwarz AG (PrüfstelleENM)"],
            ["20136", "Unterfachstelle Strasseninspektorat Emmental,Tiebauamt"],
            [
                "20118",
                "Unterfachstelle Strassenverkehrs- undSchifffahrtsamt SVSA - Abteilung Schifffahrt",
            ],
            [
                "20119",
                "Unterfachstelle Strassenverkehrs- undSchifffahrtsamt SVSA - Sonderbewilligungen",
            ],
            ["20135", "Unterfachstelle Support P+I"],
            ["20133", "Unterfachstelle SUVA - FachstellePlanvorlagen/Meldestelle DGVV"],
            ["20217", "Unterfachstelle Swisscom AG (Eggiwil)"],
            ["20222", "Unterfachstelle Swisscom AG (Hasle b. B.)"],
            ["20156", "Unterfachstelle Swisscom AG (Langnau)"],
            ["20166", "Unterfachstelle Swisscom AG (Lyssach)"],
            ["20171", "Unterfachstelle Swisscom AG (Rüderswil)"],
            ["20211", "Unterfachstelle Swisscom AG(Trubschachen)"],
            ["20194", "Unterfachstelle Swisscom AG (Wynigen)"],
            [
                "20121",
                "Unterfachstelle Tiefbauamt des Kantons Bern -Abteilung Nationalstrassen Bau",
            ],
            [
                "20120",
                "Unterfachstelle Tiefbauamt des Kantons Bern - Abteilung Nationalstrassen Betrieb",
            ],
            [
                "20122",
                "Unterfachstelle Tiefbauamt des Kantons Bern -Fachstelle Lärmschutz",
            ],
            [
                "20124",
                "Unterfachstelle Tiefbauamt des Kantons Bern -Oberingenieurkreis II - Bern Mittelland",
            ],
            [
                "20125",
                "Unterfachstelle Tiefbauamt des Kantons Bern - Oberingenieurkreis III - Seeland / Berner Jura",
            ],
            [
                "20123",
                "Unterfachstelle Tiefbauamt des Kantons Bern - Oberingenieurkreis I - Oberland",
            ],
            [
                "20126",
                "Unterfachstelle Tiefbauamt des Kantons Bern -Oberingenieurkreis IV - Oberaargau / Emmental",
            ],
            [
                "20083",
                "Unterfachstelle Unité francophone de l'OACOT –Service de l'aménagement cantonal",
            ],
            [
                "20085",
                "Unterfachstelle Unité francophone de l'OACOT -Service de l'aménagement local et régional",
            ],
            [
                "20081",
                "Unterfachstelle Unité francophone de l'OACOT -Service des constructions",
            ],
            ["20154", "Unterfachstelle Wasserversorgung Langnau(Wasseranschluss)"],
            ["20174", "Unterfachstelle WasserversorgungZollbrück"],
            ["20216", "Unterfachstelle Werner und Partner AG"],
            ["-1", "Andere"],
        ]
        return [x[1] for x in data]
