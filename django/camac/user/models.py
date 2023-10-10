import hashlib

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils.translation import gettext_lazy as _

from camac.models import dynamic_default_value

from ..core import models as core_models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "surname", "language"]

    id = models.AutoField(db_column="USER_ID", primary_key=True, verbose_name=_("ID"))
    username = models.CharField(
        db_column="USERNAME", unique=True, max_length=250, verbose_name=_("Username")
    )
    password = models.CharField(
        db_column="PASSWORD", max_length=50, blank=True, null=True
    )
    name = models.CharField(
        db_column="NAME", max_length=100, verbose_name=_("First name")
    )
    surname = models.CharField(
        db_column="SURNAME", max_length=100, verbose_name=_("Last name")
    )
    email = CIEmailField(
        db_column="EMAIL",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Email"),
    )
    phone = models.CharField(
        db_column="PHONE",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Phone"),
    )
    disabled = models.PositiveSmallIntegerField(
        db_column="DISABLED", default=0, verbose_name=_("Disabled?")
    )
    language = models.CharField(
        db_column="LANGUAGE", max_length=2, verbose_name=_("Language")
    )
    last_login = models.DateTimeField(
        db_column="LAST_REQUEST_DATE",
        blank=True,
        null=True,
        verbose_name=_("Last login"),
    )
    address = models.CharField(
        db_column="ADDRESS",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Address"),
    )
    city = models.CharField(
        db_column="CITY", max_length=100, blank=True, null=True, verbose_name=_("City")
    )
    zip = models.CharField(
        db_column="ZIP", max_length=10, blank=True, null=True, verbose_name=_("Zip")
    )
    groups = models.ManyToManyField(
        "Group",
        through="UserGroup",
        related_name="users",
        through_fields=("user", "group"),
    )

    @property
    def is_superuser(self):
        return UserGroup.objects.filter(
            user=self, group_id=settings.APPLICATION.get("ADMIN_GROUP")
        ).exists()  # pragma: no cover

    @property
    def is_staff(self):
        return self.is_superuser  # pragma: no cover

    def has_perm(self, perm):
        """
        Since we don't use the PermissionsMixin this method has to be overwritten.

        Intially this method returns True if the user has the specified permission.
        We check this in the is_superuser property.
        """
        return True  # pragma: no cover

    def has_module_perms(self, app_label):
        """
        Since we don't use the PermissionsMixin this method has to be overwritten.

        Intially this method returns True if the user has any permission in the given package.
        We check this in the is_superuser property.
        """
        return True  # pragma: no cover

    def _make_password(self, raw_password):
        salted = settings.AUTH_PASSWORT_SALT + raw_password
        return hashlib.md5(salted.encode()).hexdigest()

    def set_password(self, raw_password):
        self.password = self._make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Check password whether it matches.

        Empty passwords are not allowed.
        """
        password_empty = raw_password in ["", None]

        return not password_empty and self.password == self._make_password(raw_password)

    def get_full_name(self):
        return "{0} {1}".format(self.name, self.surname).strip()

    @property
    def is_active(self):
        return not self.disabled

    def get_default_group(self):
        user_group = UserGroup.objects.filter(user=self, default_group=True).first()
        if user_group:
            return user_group.group

    @property
    def alexandria_user(self):
        return self.id

    @property
    def alexandria_group(self):  # pragma: no cover
        group = self.get_default_group()
        if not group:
            return "-"
        if not group.service:
            return "-"
        return group.service.pk

    def __str__(self):
        return self.get_full_name()

    class Meta:
        managed = True
        db_table = "USER"
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserT(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    city = models.CharField(db_column="CITY", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "USER_T"


class Group(core_models.MultilingualModel, models.Model):
    """A group is tightly coupled to one role (with child roles) and one service/organisation (with child entities).

    It builds a link between user and service/organisation. A group has location information attached.
    Examples:
    - Admin with role Admin
    - Administration Location X with role Administration
    """

    group_id = models.AutoField(
        db_column="GROUP_ID", primary_key=True, verbose_name=_("ID")
    )
    role = models.ForeignKey(
        "user.Role",
        models.PROTECT,
        db_column="ROLE_ID",
        related_name="groups",
        verbose_name=_("Role"),
    )
    service = models.ForeignKey(
        "user.Service",
        models.SET_NULL,
        db_column="SERVICE_ID",
        related_name="groups",
        blank=True,
        null=True,
        verbose_name=_("Service"),
    )
    disabled = models.PositiveSmallIntegerField(
        db_column="DISABLED", default=0, verbose_name=_("Disabled?")
    )
    name = models.CharField(
        db_column="NAME", max_length=100, blank=True, null=True, verbose_name=_("Name")
    )
    phone = models.CharField(
        db_column="PHONE",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Phone"),
    )
    zip = models.CharField(
        db_column="ZIP", max_length=10, blank=True, null=True, verbose_name=_("Zip")
    )
    city = models.CharField(
        db_column="CITY", max_length=100, blank=True, null=True, verbose_name=_("City")
    )
    address = models.CharField(
        db_column="ADDRESS",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Address"),
    )
    email = models.CharField(
        db_column="EMAIL",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Email"),
    )
    website = models.CharField(
        db_column="WEBSITE",
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_("Website"),
    )
    locations = models.ManyToManyField(
        "Location", through="GroupLocation", verbose_name=_("Locations")
    )

    class Meta:
        managed = True
        db_table = "GROUP"
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class GroupT(models.Model):
    group = models.ForeignKey(
        Group,
        models.CASCADE,
        db_column="GROUP_ID",
        related_name="trans",
        verbose_name=_("Group"),
    )
    language = models.CharField(
        db_column="LANGUAGE", max_length=2, verbose_name=_("Language")
    )
    name = models.CharField(
        db_column="NAME", max_length=200, blank=True, null=True, verbose_name=_("Name")
    )
    city = models.CharField(
        db_column="CITY", max_length=100, blank=True, null=True, verbose_name=_("City")
    )

    class Meta:
        managed = True
        db_table = "GROUP_T"


class Location(core_models.MultilingualModel, models.Model):
    location_id = models.AutoField(db_column="LOCATION_ID", primary_key=True)
    communal_cantonal_number = models.IntegerField(
        db_column="COMMUNAL_CANTONAL_NUMBER", blank=True, null=True
    )
    communal_federal_number = models.CharField(
        db_column="COMMUNAL_FEDERAL_NUMBER", max_length=255, blank=True, null=True
    )
    district_number = models.IntegerField(
        db_column="DISTRICT_NUMBER", blank=True, null=True
    )
    section_number = models.IntegerField(
        db_column="SECTION_NUMBER", blank=True, null=True
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    commune_name = models.CharField(
        db_column="COMMUNE_NAME", max_length=100, blank=True, null=True
    )
    district_name = models.CharField(
        db_column="DISTRICT_NAME", max_length=100, blank=True, null=True
    )
    section_name = models.CharField(
        db_column="SECTION_NAME", max_length=100, blank=True, null=True
    )
    zip = models.CharField(db_column="ZIP", max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "LOCATION"


class LocationT(models.Model):
    location = models.ForeignKey(
        Location, models.CASCADE, db_column="LOCATION_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    commune_name = models.CharField(
        db_column="COMMUNE_NAME", max_length=100, blank=True, null=True
    )
    district_name = models.CharField(
        db_column="DISTRICT_NAME", max_length=100, blank=True, null=True
    )
    section_name = models.CharField(
        db_column="SECTION_NAME", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "LOCATION_T"


class GroupLocation(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    group = models.ForeignKey(
        Group,
        models.CASCADE,
        db_column="GROUP_ID",
        related_name="+",
        verbose_name=_("Group"),
    )
    location = models.ForeignKey(
        Location,
        models.CASCADE,
        db_column="LOCATION_ID",
        related_name="+",
        verbose_name=_("Location"),
    )

    class Meta:
        managed = True
        db_table = "GROUP_LOCATION"
        unique_together = (("group", "location"),)


class UserGroup(models.Model):
    """Builds the n-to-n relationship between the users and the groups."""

    id = models.AutoField(db_column="ID", primary_key=True)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        db_column="USER_ID",
        related_name="user_groups",
        verbose_name=_("User"),
    )
    group = models.ForeignKey(
        Group,
        models.CASCADE,
        db_column="GROUP_ID",
        related_name="+",
        verbose_name=_("Group"),
    )
    default_group = models.PositiveSmallIntegerField(
        db_column="DEFAULT_GROUP", verbose_name=_("Default group?")
    )
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "USER_GROUP"
        unique_together = (("user", "group"),)


class UserGroupLog(models.Model):
    user_group_log_id = models.AutoField(
        db_column="USER_GROUP_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)

    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)

    class Meta:
        managed = True
        db_table = "USER_GROUP_LOG"


class Role(core_models.MultilingualModel, models.Model):
    """Represents an organisational role which is tied to a user.

    A role can have many groups.
    Examples:
    - business specific role a person takes within an organisation entity
    - guest role or admin role (-> user.is_superuser)
    - portal visitor / customer role
    """

    role_id = models.AutoField(
        db_column="ROLE_ID", primary_key=True, verbose_name=_("ID")
    )
    role_parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        db_column="ROLE_PARENT_ID",
        related_name="+",
        blank=True,
        null=True,
        verbose_name=_("Role parent"),
    )
    name = models.CharField(
        db_column="NAME", max_length=100, blank=True, null=True, verbose_name=_("Name")
    )
    group_prefix = models.CharField(
        db_column="GROUP_PREFIX",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Group prefix"),
    )

    class Meta:
        managed = True
        db_table = "ROLE"
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


class RoleT(models.Model):
    role = models.ForeignKey(
        Role, models.CASCADE, db_column="ROLE_ID", related_name="trans"
    )
    language = models.CharField(
        db_column="LANGUAGE", max_length=2, verbose_name=_("Language")
    )
    name = models.CharField(
        db_column="NAME", max_length=100, blank=True, null=True, verbose_name=_("Name")
    )
    group_prefix = models.CharField(
        db_column="GROUP_PREFIX",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Group prefix"),
    )

    class Meta:
        managed = True
        db_table = "ROLE_T"


class ServiceGroup(core_models.MultilingualModel, models.Model):
    """The type or group membership of an organisational entity.

    Such an organisational entity belongs to exactly one service group.
    """

    service_group_id = models.AutoField(
        db_column="SERVICE_GROUP_ID", primary_key=True, verbose_name=_("ID")
    )
    name = models.CharField(
        db_column="NAME", max_length=100, blank=True, null=True, verbose_name=_("Name")
    )
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "SERVICE_GROUP"
        verbose_name = _("Service group")
        verbose_name_plural = _("Service groups")


class ServiceGroupT(models.Model):
    service_group = models.ForeignKey(
        ServiceGroup, models.CASCADE, db_column="SERVICE_GROUP_ID", related_name="trans"
    )
    language = models.CharField(
        db_column="LANGUAGE", max_length=2, verbose_name=_("Language")
    )
    name = models.CharField(
        db_column="NAME", max_length=100, blank=True, null=True, verbose_name=_("Name")
    )

    class Meta:
        managed = True
        db_table = "SERVICE_GROUP_T"


@dynamic_default_value(0)
def next_service_sort():
    last_service = Service.objects.order_by("-sort").first()
    return last_service.sort + 1 if last_service else 0


class Service(core_models.MultilingualModel, models.Model):
    """Represents an organisational entity which can be hierarchically structured.

    A service has one service group. A service is bound to roles via the group table:
    Remember that a group has also location information like a service, and links to roles:

    - `service.group.roles`

    Examples:
    - Leitbehörde Woppeln
    """

    service_id = models.AutoField(
        db_column="SERVICE_ID", primary_key=True, verbose_name=_("ID")
    )
    service_group = models.ForeignKey(
        ServiceGroup,
        models.PROTECT,
        db_column="SERVICE_GROUP_ID",
        related_name="+",
        verbose_name=_("Service group"),
    )
    service_parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        db_column="SERVICE_PARENT_ID",
        related_name="service_children",
        blank=True,
        null=True,
        verbose_name=_("Service parent"),
    )
    name = models.CharField(
        db_column="NAME", max_length=100, blank=True, null=True, verbose_name=_("Name")
    )
    description = models.CharField(
        db_column="DESCRIPTION",
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )
    sort = models.IntegerField(db_column="SORT", default=next_service_sort)
    phone = models.CharField(
        db_column="PHONE",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Phone"),
    )
    zip = models.CharField(
        db_column="ZIP", max_length=10, blank=True, null=True, verbose_name=_("Zip")
    )
    city = models.CharField(
        db_column="CITY", max_length=100, blank=True, null=True, verbose_name=_("City")
    )
    address = models.CharField(
        db_column="ADDRESS",
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Address"),
    )
    email = models.CharField(
        db_column="EMAIL",
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_("Email"),
    )
    website = models.CharField(
        db_column="WEBSITE",
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_("Website"),
    )
    disabled = models.PositiveSmallIntegerField(
        db_column="DISABLED", default=0, verbose_name=_("Disabled?")
    )
    notification = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Receive notifications?")
    )
    responsibility_construction_control = models.BooleanField(
        default=False, verbose_name=_("Apply responsibility in construction control?")
    )

    class Meta:
        managed = True
        db_table = "SERVICE"
        ordering = ["service_group__name"]
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class ServiceT(models.Model):
    service = models.ForeignKey(
        Service, models.CASCADE, db_column="SERVICE_ID", related_name="trans"
    )
    language = models.CharField(
        db_column="LANGUAGE", max_length=2, verbose_name=_("Language")
    )
    name = models.CharField(
        db_column="NAME", max_length=200, blank=True, null=True, verbose_name=_("Name")
    )
    description = models.CharField(
        db_column="DESCRIPTION",
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )
    city = models.CharField(
        db_column="CITY", max_length=100, blank=True, null=True, verbose_name=_("City")
    )

    class Meta:
        managed = True
        db_table = "SERVICE_T"
