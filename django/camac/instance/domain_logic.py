from camac.user.permissions import permission_aware
from django.conf import settings


class CreateInstanceLogic:
    @staticmethod
    def validate(data, group):
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        perm = perms.get(group.role.name) if group else "public"
        permission_func = getattr(CreateInstanceLogic, f"validate_for_{perm}")

        return permission_func(data, group) if permission_func else data

    @staticmethod
    def validate_for_municipality(data, group):
        if settings.APPLICATION["CALUMA"].get("CREATE_IN_PROCESS"):
            data["instance_state"] = models.InstanceState.objects.get(name="comm")

        if settings.APPLICATION["CALUMA"].get("USE_LOCATION"):
            if (
                data.get("location", False)
                and data["location"] not in group.locations.all()
            ):
                raise ValidationError(
                    "Provided location is not present in group locations"
                )

            data["location"] = data.get("location", group.locations.first())

        return data

    @staticmethod
    def validate_for_coordination(data, group):  # pragma: no cover
        if settings.APPLICATION["CALUMA"].get("CREATE_IN_PROCESS"):
            # FIXME: Bundesstelle has role "coordination, but is
            # actually more like a municipality (dossiers start in COMM)
            is_federal = group.service.pk == ur_constants.BUNDESSTELLE_SERVICE_ID
            state = "comm" if is_federal else "ext"
            data["instance_state"] = models.InstanceState.objects.get(name=state)

        return data

    @staticmethod
    def pre_create(validated_data, user, context=None):
        pass

    @staticmethod
    def post_create(case, user, parent_work_item, context=None):
        pass
