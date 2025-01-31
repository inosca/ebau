from rest_framework import serializers

from camac.instance.master_data import MasterData
from camac.instance.serializers import InstanceStateSerializer
from camac.user.models import Service


class EebaExportSerializer(serializers.Serializer):
    def __init__(self, case, *args, **kwargs):
        super().__init__(case, *args, **kwargs)
        self.master_data = MasterData(case)

    # Deviation from PEP8 (not using snake_case for the fields)
    # because of specifications from eeba
    ebauId = serializers.SerializerMethodField()
    statusName = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()
    landowner = serializers.SerializerMethodField()
    projectAuthor = serializers.SerializerMethodField()
    invoiceRecipient = serializers.SerializerMethodField()
    plots = serializers.SerializerMethodField()
    volumes = serializers.SerializerMethodField()

    def get_ebauId(self, case):
        return case.instance.pk

    def get_statusName(self, case):
        # use  MultilingualSerializer
        return InstanceStateSerializer(case.instance.instance_state).data.get("name")

    def _get_person(self, person_type):
        persons = getattr(self.master_data, person_type, [])

        if not persons:
            return None  # pragma: no cover

        person = persons[0]

        return {
            "juristicName": person.get("juristic_name"),
            "firstName": person.get("first_name"),
            "lastName": person.get("last_name"),
            "street": person.get("street"),
            "streetNumber": person.get("street_number"),
            "zip": person.get("zip"),
            "city": person.get("town"),
            "phone": person.get("tel"),
            "email": person.get("email"),
        }

    def get_applicant(self, case):
        return self._get_person("applicants")

    def get_landowner(self, case):
        return self._get_person("landowners")

    def get_projectAuthor(self, case):
        return self._get_person("project_authors")

    def get_invoiceRecipient(self, case):
        return self._get_person("invoice_recipients")

    def get_plots(self, case):
        service = Service.objects.filter(pk=self.master_data.municipality_slug).first()
        bfs_number = service.external_identifier if service else None

        return [
            {"number": plot.get("plot_number"), "bfsNumber": bfs_number}
            for plot in self.master_data.plot_data
        ]

    def _get_soiling_suspicion(self):
        construction_zone = self.master_data.construction_zone
        return (
            construction_zone
            and "das-bauvorhaben-befindet-sich-in-kataster-belasteter-standorte"
            in construction_zone
        )

    def get_volumes(self, case):
        return {
            "deconstructionMaterial": self.master_data.deconstruction_material,
            "removedTopsoil": self.master_data.removed_topsoil,
            "excavation": self.master_data.excavation,
            "roadSurface": self.master_data.road_surface,
            "trackExcavation": self.master_data.track_excavation,
            "yearOfConstructionCases": self.master_data.year_of_construction_oldest_affected_object,
            "soilingSuspicion": self._get_soiling_suspicion(),
        }
