from django.utils import timezone
from rest_framework import serializers

from camac.instance.master_data import MasterData


def complete_floor(dwelling):
    if dwelling.get("floor_type") == 3100:
        return 3100

    if dwelling.get("floor_type") and dwelling.get("floor_number"):
        return dwelling.get("floor_type") + int(dwelling.get("floor_number")) - 1

    return None  # pragma: no cover


def to_int(string):
    return int(string) if string else None


class GwrSerializer(serializers.Serializer):
    def __init__(self, case, *args, **kwargs):
        super().__init__(case, *args, **kwargs)
        self.master_data = MasterData(case)

    officialConstructionProjectFileNo = serializers.SerializerMethodField()

    typeOfClient = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    typeOfConstructionProject = serializers.SerializerMethodField()
    constructionProjectDescription = serializers.SerializerMethodField()
    constructionLocalisation = serializers.SerializerMethodField()
    typeOfConstruction = serializers.SerializerMethodField()
    typeOfPermit = serializers.SerializerMethodField()
    totalCostsOfProject = serializers.SerializerMethodField()
    realestateIdentification = serializers.SerializerMethodField()

    projectAnnouncementDate = serializers.SerializerMethodField()
    buildingPermitIssueDate = serializers.SerializerMethodField()
    projectStartDate = serializers.SerializerMethodField()
    projectCompletionDate = serializers.SerializerMethodField()
    work = serializers.SerializerMethodField()

    def get_client(self, case):
        applicants = self.master_data.applicants

        if not applicants or not len(applicants):
            return None

        applicant = applicants[0]

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
                }
                if not applicant.get("is_juristic_person")
                else None,
                "isOrganisation": applicant.get("is_juristic_person"),
                "organisationIdentification": {
                    "organisationName": applicant.get("juristic_name")
                    if applicant.get("is_juristic_person")
                    else None
                },
            },
        }

    def get_officialConstructionProjectFileNo(self, case):
        # TODO Configure this for SZ
        try:
            return self.master_data.dossier_number
        except AttributeError:  # pragma: no cover
            return None

    def get_constructionProjectDescription(self, case):
        return self.master_data.proposal

    def get_constructionLocalisation(self, case):
        # TODO Configure this for SZ
        try:
            return {"municipalityName": self.master_data.municipality.get("label")}
        except AttributeError:  # pragma: no cover
            return None

    def get_typeOfConstructionProject(self, case):
        # TODO Configure this for BE and SZ
        try:
            return self.master_data.category[0]
        except (AttributeError, IndexError):  # pragma: no cover
            return None

    def get_typeOfConstruction(self, case):
        # TODO Configure this for BE and SZ
        try:
            return self.master_data.type_of_construction[0]["art_der_hochbaute"]
        except (AttributeError, IndexError):  # pragma: no cover
            return None

    def get_totalCostsOfProject(self, case):
        return self.master_data.construction_costs

    def get_realestateIdentification(self, case):
        # TODO Configure this for SZ
        try:
            plot_data = self.master_data.plot_data[0]
            return {
                "number": plot_data.get("plot_number"),
                "EGRID": plot_data.get("egrid_number"),
            }
        except (AttributeError, IndexError):  # pragma: no cover
            return None

    def get_projectAnnouncementDate(self, case):
        submit_date = self.master_data.submit_date
        return submit_date.date().isoformat() if submit_date else None

    def get_buildingPermitIssueDate(self, case):
        # TODO Configure this for BE and SZ
        try:
            decision_date = self.master_data.decision_date
            return decision_date.date().isoformat() if decision_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_projectStartDate(self, case):
        # TODO Configure this for BE and SZ
        try:
            start_date = self.master_data.construction_start_date
            return start_date.date().isoformat() if start_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_projectCompletionDate(self, case):
        # TODO Configure this for BE and SZ
        try:
            end_date = self.master_data.construction_end_date
            return end_date.date().isoformat() if end_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_energy_device(self, building, is_heating, is_main_heating):
        heating_type = "is_heating" if is_heating else "is_warm_water"
        building_name = building.get("name")
        return next(
            (
                {
                    "energySourceHeating": device.get("energy_source"),
                    "informationSourceHeating": device.get("information_source"),
                    "revisionDate": timezone.now().date(),
                }
                for device in self.master_data.energy_devices
                if device.get(heating_type)
                and device.get("name_of_building") == building_name
                and device.get("is_main_heating") == is_main_heating
            ),
            None,
        )

    def get_work(self, case):
        # TODO Configure this for BE and SZ
        try:
            buildings = self.master_data.buildings
            dwellings = self.master_data.dwellings

            plot_data = self.master_data.plot_data
            plot_data = plot_data[0] if len(plot_data) else None
            construction_end_date = self.master_data.construction_end_date

            return [
                {
                    "kindOfWork": building["proposal"][0]
                    if building["proposal"] and len(building["proposal"])
                    else None,
                    "building": {
                        "nameOfBuilding": building.get("name"),
                        "buildingCategory": building.get("building_category"),
                        "dateOfConstruction": {
                            "yearMonthDay": construction_end_date.date().isoformat()
                        }
                        if 6001 in building.get("proposal") and construction_end_date
                        else None,
                        "thermotechnicalDeviceForHeating1": self.get_energy_device(
                            building, is_heating=True, is_main_heating=True
                        ),
                        "thermotechnicalDeviceForHeating2": self.get_energy_device(
                            building, is_heating=True, is_main_heating=False
                        ),
                        "thermotechnicalDeviceForWarmWater1": self.get_energy_device(
                            building, is_heating=False, is_main_heating=True
                        ),
                        "thermotechnicalDeviceForWarmWater2": self.get_energy_device(
                            building, is_heating=False, is_main_heating=False
                        ),
                        "realestateIdentification": {
                            "number": plot_data.get("plot_number"),
                            "EGRID": plot_data.get("egrid_number"),
                        }
                        if plot_data
                        else None,
                        "dwellings": [
                            {
                                "floor": complete_floor(dwelling),
                                "floorType": dwelling.get("floor_type"),
                                "floorNumber": to_int(dwelling.get("floor_number")),
                                "locationOfDwellingOnFloor": dwelling.get(
                                    "location_on_floor"
                                ),
                                "noOfHabitableRooms": dwelling.get("number_of_rooms"),
                                "kitchen": dwelling.get("has_kitchen_facilities"),
                                "surfaceAreaOfDwelling": dwelling.get("area"),
                                "multipleFloor": dwelling.get("multiple_floors"),
                                "usageLimitation": dwelling.get("usage_limitation"),
                            }
                            for dwelling in dwellings
                            if dwelling.get("name_of_building") == building.get("name")
                        ],
                    },
                }
                for building in buildings
            ]
        except (AttributeError, IndexError):  # pragma: no cover
            return []

    def get_typeOfPermit(self, case):
        # TODO Configure this for BE and SZ
        try:
            reason = self.master_data.approval_reason
            return int(reason) if reason else None
        except AttributeError:  # pragma: no cover
            return None

    def get_typeOfClient(self, case):
        # TODO Configure this for BE and SZ
        try:
            type_of_applicant = self.master_data.type_of_applicant
            return int(type_of_applicant) if type_of_applicant else None
        except AttributeError:  # pragma: no cover
            return None
