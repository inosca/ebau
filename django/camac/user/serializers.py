from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Document, Question
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language, gettext as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import BooleanField
from rest_framework.serializers import Serializer as RestSerializer, ValidationError
from rest_framework_json_api import relations, serializers

from camac.core.serializers import MultilingualField, MultilingualSerializer
from camac.fields import CamacBooleanField
from camac.instance.utils import get_lead_authority
from camac.notification.utils import send_mail_without_instance
from camac.user.relations import CurrentUserResourceRelatedField

from . import models


class CurrentGroupDefault(object):
    requires_context = True

    def __call__(self, serializer_field):
        # When generating the schema with our custom FileUploadSwaggerAutoSchema
        # we don't have access to the request object
        return (
            serializer_field.context["request"].group
            if "request" in serializer_field.context
            else None
        )

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class CurrentServiceDefault(object):
    requires_context = True

    def __call__(self, serializer_field):
        # When generating the schema with our custom FileUploadSwaggerAutoSchema
        # we don't have access to the request object
        request = serializer_field.context.get("request")

        return (
            request.group.service
            if request and not isinstance(request.user, AnonymousUser)
            else None
        )

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class UserSerializer(serializers.ModelSerializer):
    service = relations.SerializerMethodResourceRelatedField(
        source="get_service", model=models.Service, read_only=True
    )

    def get_service(self, obj):
        request = self.context["request"]
        return request.group and request.group.service or None

    class Meta:
        model = get_user_model()
        fields = (
            "name",
            "surname",
            "username",
            "language",
            "service",
            "email",
            "phone",
        )


class CurrentUserSerializer(UserSerializer):
    groups = relations.SerializerMethodResourceRelatedField(
        source="get_groups", model=models.Group, read_only=True, many=True
    )
    default_group = relations.SerializerMethodResourceRelatedField(
        source="get_default_group", model=models.Group, read_only=True
    )

    def get_groups(self, obj):
        return obj.groups.filter(disabled=False)

    def get_default_group(self, obj):
        return obj.get_default_group()

    included_serializers = {
        "groups": "camac.user.serializers.GroupSerializer",
        "service": "camac.user.serializers.ServiceSerializer",
    }

    def get_extra_kwargs(self):
        """Override read_only property for editable fields.

        By default, all fields must be read only to make sure updating of an
        user is only possible for the properties that are explicitly configured
        and are not being synced with OIDC.
        """

        extra_kwargs = super().get_extra_kwargs()

        if not settings.USER.allowed_write_attributes:
            return extra_kwargs

        for field_name in settings.USER.allowed_write_attributes:
            if (
                field_name in settings.APPLICATION.get("OIDC_SYNC_USER_ATTRIBUTES")
                or field_name not in extra_kwargs
            ):
                continue

            extra_kwargs[field_name]["read_only"] = False

        return extra_kwargs

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "groups",
            "default_group",
            "address",
            "zip",
            "city",
            "title",
            "position",
            "mobile",
            "division",
        )
        read_only_fields = UserSerializer.Meta.fields + (
            "groups",
            "default_group",
            "address",
            "zip",
            "city",
            "title",
            "position",
            "mobile",
            "division",
        )


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username", "name", "surname")
        resource_name = "public-users"


class RoleSerializer(MultilingualSerializer, serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    def get_permission(self, role):
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        return perms.get(role.name)

    class Meta:
        model = models.Role
        fields = ("name", "permission", "slug")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number", "zip")


class ServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    city = MultilingualField()
    description = MultilingualField()
    department = MultilingualField(required=False, allow_null=True)
    users = relations.SerializerMethodResourceRelatedField(
        source="get_users", model=models.User, read_only=True, many=True
    )
    municipality = relations.SerializerMethodResourceRelatedField(
        source="get_municipality", model=models.Service, read_only=True
    )
    notification = CamacBooleanField(default=True)
    disabled = CamacBooleanField(default=False)
    uses_ech_api = CamacBooleanField(default=False)
    responsibility_construction_control = BooleanField(default=False)

    def get_users(self, obj):
        return models.User.objects.filter(
            user_groups__group_id__in=obj.groups.values("pk")
        ).distinct()

    def get_municipality(self, obj):
        try:
            return (
                get_lead_authority(obj)
                if obj.service_group.name == "construction-control"
                else None
            )
        except Exception:
            print(
                _(
                    "Could not find lead authority for construction control %(id)d"
                    % {"id": obj.pk}
                )
            )
            return None

    included_serializers = {
        "users": "camac.user.serializers.UserSerializer",
        "service_parent": "camac.user.serializers.ServiceSerializer",
        "service_group": "camac.user.serializers.PublicServiceGroupSerializer",
        "municipality": "camac.user.serializers.ServiceSerializer",
    }

    def validate_name(self, value):
        old_name = self.instance.get_name() if self.instance else None

        multilang = settings.APPLICATION.get("IS_MULTILINGUAL")

        if old_name != value and (
            (
                multilang
                and models.ServiceT.objects.filter(
                    name=value, language=get_language()
                ).exists()
            )
            or (not multilang and models.Service.objects.filter(name=value).exists())
        ):
            raise ValidationError(_("There is already a service with this name"))

        return value

    def validate_email(self, value):
        emails = [email.lower().strip() for email in value.split(",")]
        for email in emails:
            validate_email(email)
        return ",".join(emails)

    def get_group_name(self, service_name, role):
        prefix = role.get_trans_attr("group_prefix")

        return f"{prefix} {service_name}" if prefix else service_name

    @transaction.atomic
    def create(self, validated_data):
        parent = self.context["request"].group.service

        name = validated_data["name"]
        city = validated_data["city"]
        description = validated_data["description"]
        department = validated_data.get("department", None)

        validated_data["service_parent"] = parent
        validated_data["service_group"] = parent.service_group

        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            validated_data.pop("name")
            validated_data.pop("city")
            validated_data.pop("description")
            validated_data.pop("department", None)

        service = super().create(validated_data)

        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            language = get_language()
            models.ServiceT.objects.create(
                service=service,
                language=language,
                name=name,
                city=city,
                description=description,
                department=department,
            )
            # If no translation is defined for a multilingual model in the current language,
            # it uses the fallback language. Create a fallback translation, to ensure that
            # the application doesn't run into issues for the other languages that have no
            # translation defined.
            if not language == settings.LANGUAGE_CODE:  # pragma: todo cover
                models.ServiceT.objects.create(
                    service=service,
                    language=settings.LANGUAGE_CODE,
                    name=name,
                    city=city,
                    description=description,
                    department=department,
                )

        # Create a group for each role that is defined as subservice role
        for role_name in settings.APPLICATION.get("SUBSERVICE_ROLES", []):
            role = models.Role.objects.get(name=role_name)
            name = self.get_group_name(name, role)

            group = models.Group.objects.create(
                service=service,
                role=role,
                name=(None if settings.APPLICATION.get("IS_MULTILINGUAL") else name),
            )

            if settings.APPLICATION.get("IS_MULTILINGUAL"):
                models.GroupT.objects.create(
                    group=group,
                    name=name,
                    language=get_language(),
                )

                # Create a fallback translation, to ensure that the application doesn't run
                # into issues for the other languages that have no translation defined.
                if not language == settings.LANGUAGE_CODE:  # pragma: todo cover
                    models.GroupT.objects.create(
                        group=group,
                        name=name,
                        language=settings.LANGUAGE_CODE,
                    )

        return service

    @transaction.atomic
    def update(self, instance, validated_data):  # noqa: C901
        old_name = instance.get_name()
        new_name = validated_data.get("name", old_name)

        old_description = instance.get_trans_attr("description")
        new_description = validated_data.get("description", old_description)

        old_city = instance.get_trans_attr("city")
        new_city = validated_data.get("city", old_city)

        old_department = instance.get_trans_attr("department")
        new_department = validated_data.get("department", old_department)

        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            validated_data.pop("name", None)
            validated_data.pop("description", None)
            validated_data.pop("city", None)
            validated_data.pop("department", None)

        instance = super().update(instance, validated_data)

        language = get_language()
        # If a new service translation will be created for the language, perform
        # the update, even though the old and new values may be the same
        create_new_translation = False
        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            service_t = instance.get_trans_obj()
            create_new_translation = service_t.language != language

        if (
            all(
                (
                    old_name == new_name,
                    old_description == new_description,
                    old_city == new_city,
                    old_department == new_department,
                )
            )
            and not create_new_translation
        ):  # pragma: no cover
            return instance

        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            service_t = instance.get_trans_obj()
            # If there is no service translation defined for the current language
            # we create a new service translation to edit, instead of editing the
            # fallback translation
            if service_t and not service_t.language == language:  # pragma: todo cover
                models.ServiceT.objects.create(
                    service=instance,
                    language=language,
                    name=new_name,
                    city=new_city,
                    description=new_description,
                    department=new_department,
                )
            elif service_t:
                service_t.name = new_name
                service_t.description = new_description
                service_t.city = new_city
                service_t.department = new_department
                service_t.save()

        if old_name != new_name and settings.APPLICATION.get(
            "GROUP_RENAME_ON_SERVICE_RENAME", False
        ):
            for group in instance.groups.iterator():
                name = self.get_group_name(new_name, group.role)
                if settings.APPLICATION.get("IS_MULTILINGUAL"):
                    group_t = group.get_trans_obj()
                    if (
                        group_t and not group_t.language == language
                    ):  # pragma: todo cover
                        models.GroupT.objects.create(
                            group=group, name=name, language=language
                        )
                    elif group_t:
                        group_t.name = name
                        group_t.save()

                else:
                    group.name = name
                    group.save()

        return instance

    class Meta:
        model = models.Service
        fields = (
            "name",
            "description",
            "email",
            "notification",
            "zip",
            "city",
            "address",
            "phone",
            "users",
            "service_parent",
            "service_group",
            "sort",
            "website",
            "municipality",
            "responsibility_construction_control",
            "disabled",
            "logo",
            "slug",
            "department",
            "uses_ech_api",
        )
        read_only_fields = (
            "users",
            "sort",
            "service_parent",
            "service_group",
            "municipality",
            "logo",
            "slug",
        )


class GroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {
        "users": UserSerializer,
        "service": ServiceSerializer,
        "role": RoleSerializer,
        "locations": LocationSerializer,
    }
    users = relations.SerializerMethodResourceRelatedField(
        source="get_users", model=models.User, read_only=True, many=True
    )

    def get_users(self, obj):
        return obj.users.filter(disabled=False)

    class Meta:
        model = models.Group
        fields = ("name", "users", "service", "role", "locations")


class PublicRoleSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ("name", "slug")
        resource_name = "public-role"


class PublicServiceGroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.ServiceGroup
        fields = (
            "name",
            "slug",
        )
        resource_name = "public-service-groups"


class PublicServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {"service_group": PublicServiceGroupSerializer}

    class Meta:
        model = models.Service
        fields = (
            "name",
            "website",
            "service_group",
            "logo",
            "uses_ech_api",
        )
        resource_name = "public-services"


class PublicMunicipalitySerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = (
            "name",
            "website",
            "email",
            "phone",
        )
        resource_name = "public-municipalities"


class PublicGroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {
        "service": PublicServiceSerializer,
        "role": PublicRoleSerializer,
    }

    class Meta:
        model = models.Group
        fields = ("name", "service", "role")
        resource_name = "public-groups"


class UserGroupInvitationSerializer(serializers.ModelSerializer):
    created_by = CurrentUserResourceRelatedField()
    included_serializers = {
        "group": GroupSerializer,
        "created_by": UserSerializer,
    }

    def validate(self, validated_data):
        group = validated_data["group"]
        service = (
            self.context["request"].group.service
            if self.context["request"].group
            else None
        )

        if group.service != service and group.service.service_parent != service:
            # User does not have permission to add a user to this group
            raise PermissionDenied()

        return validated_data

    @transaction.atomic
    def create(self, validated_data):
        invitation = super().create(validated_data)

        if (
            notification := getattr(settings.USER.notifications, "user_invited", None)
        ) and not (
            models.UserGroupInvitation.objects.filter(email=invitation.email)
            .filter(expires_at__gt=timezone.now())
            .exclude(pk=invitation.pk)
            .exists()
        ):
            send_mail_without_instance(
                notification,
                recipients=[validated_data.get("email")],
                additional_placeholders={
                    "INVITED_TO_SERVICE": invitation.group.service.get_name()
                },
            )

        return invitation

    class Meta:
        model = models.UserGroupInvitation
        fields = (
            "email",
            "group",
            "created_at",
            "created_by",
            "expires_at",
        )
        read_only_fields = (
            "created_at",
            "created_by",
        )


class UserGroupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    created_by = CurrentUserResourceRelatedField()

    included_serializers = {
        "user": UserSerializer,
        "group": GroupSerializer,
        "created_by": UserSerializer,
    }

    def _invitable_users_qs(self):
        queryset = models.User.objects.filter(disabled=0)

        if settings.ENABLE_TOKEN_EXCHANGE:
            # If token exchange is enabled, we need to make sure that only
            # users **not** using that login method can be granted access to
            # a group.
            queryset = queryset.exclude(
                username__startswith=settings.TOKEN_EXCHANGE_USERNAME_PREFIX
            )
        return queryset

    def validate_email(self, value):
        try:
            self._invitable_users_qs().get(email=value)
        except models.User.DoesNotExist:
            raise ValidationError(
                _(
                    "No user with this email address found. Please make sure"
                    "the person already has an account with this email address"
                    "or check the spelling of the email address."
                ),
                "not_found",
            )
        except models.User.MultipleObjectsReturned:
            raise ValidationError(_("Multiple users with that email exist"))

        return value

    def validate(self, validated_data):
        group = validated_data["group"]
        service = (
            self.context["request"].group.service
            if self.context["request"].group
            else None
        )

        user = self._invitable_users_qs().get(email=validated_data.pop("email"))

        if models.UserGroup.objects.filter(group=group, user=user).exists():
            raise ValidationError(_("User is already in group"))

        # User does not have permission to add a user to this group
        if group.service != service and group.service.service_parent != service:
            raise PermissionDenied()

        validated_data.update({"user": user, "default_group": 0})

        return validated_data

    class Meta:
        model = models.UserGroup
        fields = (
            "email",
            "group",
            "user",
            "created_at",
            "created_by",
        )
        read_only_fields = (
            "user",
            "created_at",
            "created_by",
        )


class KeycloakApplySerializer(RestSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects)

    def _write_answer(self, document, question_slug, value):
        if not value:  #  pragma: no cover
            return

        try:
            question = Question.objects.get(pk=question_slug)
        except Question.DoesNotExist:  # pragma: no cover
            return False

        save_answer(
            question=question,
            document=document,
            user=self.context["request"].caluma_info.context.user,
            value=int(value) if question.type == Question.TYPE_INTEGER else str(value),
        )

        return True

    def create(self, validated_data):
        user = self.context["request"].user
        document = validated_data["document"]
        written_questions = set()

        for (
            question_slug,
            attributes,
        ) in settings.USER.question_user_attributes_mapping.items():
            if not isinstance(attributes, list):
                attributes = [attributes]

            value = ""
            for attr in attributes:
                value = getattr(user, attr)

                if value:
                    # If the attribute is not empty, we don't check the next
                    # attribute at all.
                    break

            success = self._write_answer(document, question_slug, value)

            if success:
                written_questions.add(question_slug)

        return {"document": document, "questions": written_questions}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["questions"] = instance["questions"]
        return rep


class MergeMunicipalityMappingSerializer(serializers.Serializer):
    from_service = serializers.IntegerField()
    to_service = serializers.IntegerField(allow_null=True, required=False)
    action = serializers.ChoiceField(choices=["merge", "adopt"])

    def validate(self, data):
        action = data.get("action")
        to_service = data.get("to_service")

        if action == "merge" and to_service is None:
            raise serializers.ValidationError(
                {"to_service": "This field is required when action is 'merge'."}
            )
        elif action == "adopt" and to_service is not None:
            raise serializers.ValidationError(
                {"to_service": "This field is not allowed when action is 'adopt'."}
            )

        return data


class MergeMunicipalitySerializer(serializers.Serializer):
    from_municipality = serializers.IntegerField()
    to_municipality = serializers.IntegerField()
    mapping = serializers.ListField(child=MergeMunicipalityMappingSerializer())

    def validate(self, data):
        from_municipality_pk = data.get("from_municipality")
        to_municipality_pk = data.get("to_municipality")
        mapping = data.get("mapping")

        from_municipality, to_municipality = self._validate_municipalities(
            from_municipality_pk, to_municipality_pk
        )
        data["from_municipality"] = from_municipality
        data["to_municipality"] = to_municipality

        resolved_mapping = []
        for entry in mapping:
            from_service, to_service, action = self._validate_mapping_entry(
                from_municipality, to_municipality, entry
            )

            resolved_mapping.append(
                {
                    "action": action,
                    "from_service": from_service,
                    "to_service": to_service,
                }
            )

        data["mapping"] = resolved_mapping

        return data

    def _validate_municipalities(self, from_municipality_pk, to_municipality_pk):
        queryset = models.Service.objects.filter(service_group__name="municipality")
        from_municipality = queryset.filter(pk=from_municipality_pk).first()
        to_municipality = queryset.filter(pk=to_municipality_pk).first()

        if not from_municipality or not to_municipality:
            raise serializers.ValidationError(
                "Could not find one or both of the municipalities"
            )

        if from_municipality == to_municipality:
            raise serializers.ValidationError("Cannot merge a municipality with itself")

        return from_municipality, to_municipality

    def _validate_mapping_entry(self, from_municipality, to_municipality, entry):
        from_service_pk = entry.get("from_service")
        to_service_pk = entry.get("to_service")
        action = entry.get("action")

        queryset_from = models.Service.objects.filter(service_parent=from_municipality)
        queryset_to = models.Service.objects.filter(service_parent=to_municipality)

        if action == "merge" and from_service_pk == to_service_pk:
            raise serializers.ValidationError("Cannot merge a service with itself")

        if action == "merge":
            from_service = queryset_from.filter(pk=from_service_pk).first()
            to_service = queryset_to.filter(pk=to_service_pk).first()
        elif action == "adopt":
            from_service = queryset_from.filter(pk=from_service_pk).first()
            to_service = from_service

        if not from_service or not to_service:
            raise serializers.ValidationError(
                "Could not find one or both of the services to merge"
            )

        return from_service, to_service, action
