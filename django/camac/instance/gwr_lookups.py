from rest_framework import serializers

from camac.instance.master_data import MasterData


class GwrSerializer(serializers.Serializer):
    def __init__(self, case, *args, **kwargs):
        super().__init__(case, *args, **kwargs)
        self.master_data = MasterData(case)

    client = serializers.SerializerMethodField()
    officialConstructionProjectFileNo = serializers.SerializerMethodField()
    constructionProjectDescription = serializers.SerializerMethodField()
    constructionLocalisation = serializers.SerializerMethodField()
    typeOfConstructionProject = serializers.SerializerMethodField()
    typeOfConstruction = serializers.SerializerMethodField()
    totalCostsOfProject = serializers.SerializerMethodField()
    realestateIdentification = serializers.SerializerMethodField()
    projectAnnouncementDate = serializers.SerializerMethodField()

    def get_client(self, case):
        applicant = self.master_data.applicants[0]
        return {
            "address": {
                "town": applicant.get("town"),
                "swissZipCode": applicant.get("zip"),
                "street": applicant.get("street"),
                "houseNumber": applicant.get("street_number"),
                "country": applicant.get("country"),
            },
            "identification": {
                "personIdentification": {
                    "officialName": applicant.get("last_name"),
                    "firstName": applicant.get("first_name"),
                },
                "isOrganisation": applicant.get("is_juristic_person"),
                "organisationIdentification": {
                    "organisationName": applicant.get("juristic_name")
                    if applicant.get("is_juristic_person")
                    else None
                },
            },
        }

    def get_officialConstructionProjectFileNo(self, case):
        return self.master_data.dossier_number

    def get_constructionProjectDescription(self, case):
        return self.master_data.proposal

    def get_constructionLocalisation(self, case):
        return {"municipalityName": self.master_data.municipality.get("label")}

    def get_typeOfConstructionProject(self, case):
        # TODO Configure this for bern
        try:
            return self.master_data.category
        except AttributeError:  # pragma: no cover
            return None

    def get_typeOfConstruction(self, case):
        # TODO Configure this for bern
        try:
            return self.master_data.type_of_construction
        except AttributeError:  # pragma: no cover
            return None

    def get_totalCostsOfProject(self, case):
        return self.master_data.construction_costs

    def get_realestateIdentification(self, case):
        plot_data = self.master_data.plot_data[0]
        return {
            "number": plot_data["plot_number"],
            "EGRID": plot_data["egrid_number"],
        }

    def get_projectAnnouncementDate(self, case):
        return self.master_data.submit_date.date().isoformat()
