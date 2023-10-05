from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Service


class Command(BaseCommand):
    help = "Set sort number for services"

    @transaction.atomic
    def handle(self, *args, **options):
        service_sort_number = {
            "Amt für Raumentwicklung (Ortsplanung)": 1,
            "Amt für Raumentwicklung (Kantonale Planung)": 2,
            "Amt für Landwirtschaft": 3,
            "Amt für Arbeit": 4,
            "Tiefbauamt": 5,
            "Tiefbauamt des Kantons Schwyz": 5,
            "Verkehrsamt": 6,
            "Amt für öffentlichen Verkehr": 7,
            "Amt für Umwelt und Energie": 8,
            "Amt für Gewässer": 9,
            "Amt für Wald und Natur": 10,
            "Amt für Militär, Feuer- und Zivilschutz (Brandschutz)": 11,
            "Amt für Militär, Feuer- und Zivilschutz (Zivilschutz)": 12,
            "Laboratorium der Urkantone": 13,
            "Kantonspolizei (Fachdienst Verkehr)": 14,
            "Amt für Kultur": 15,
            "Bezirk Höfe": 16,
            "Bezirk Höfe Gewässerkommission": 17,
            "Bezirk March (Gewässer)": 18,
            "Bezirk March (Strassen)": 19,
            "Bezirk Schwyz (Gewässer)": 20,
            "Bezirk Schwyz (Strassen)": 21,
            "Schweizerische Bundesbahnen AG Olten": 22,
            "Schweizerische Bundesbahnen AG Zürich": 23,
            "Schweizerische Südostbahn AG": 24,
            "Rigi Bahnen AG": 25,
            "Linthebene Melioration": 26,
            "Linthverwaltung": 27,
            "Swissgrid AG": 28,
            "Axpo Grid AG": 29,
            "AXPO Power AG": 29,
            "Centralschweizerische Kraftwerke AG": 30,
            "ebs Energie AG": 31,
            "EWS AG": 32,
            "Elektrizitätswerk der Stadt Zürich": 33,
            "Elektrizitätswerke des Kantons Zürich": 34,
            "EWA energieUri AG": 35,
            "Elektrogenossenschaft Bisisthal": 36,
            "Eidg. Starkstrominspektorat": 37,
            "Bundesamt für Strassen Winterthur": 38,
            "Bundesamt für Strassen Zofingen": 39,
            "Bundesamt für Umwelt": 40,
            "Bundesamt für Verkehr": 41,
            "Bundesamt für Zivilluftfahrt (BAZL)": 42,
            "IKSS": 43,
            "Schifffahrtsgesellschaft des Vierwaldstättersees": 44,
            "Schifffahrtsgesellschaft für den Zugersee AG": 45,
            "Zürichsee Schifffahrtsgesellschaft": 46,
            "Schiessoffizier": 47,
        }

        services_to_sort = Service.objects.filter(name__in=service_sort_number.keys())

        for service in services_to_sort:
            service.sort = service_sort_number[service.name]
            service.save()
