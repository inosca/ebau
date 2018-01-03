import hashlib

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'name', 'surname', 'language'
    ]

    id = models.AutoField(db_column='USER_ID', primary_key=True)
    username = models.CharField(
        db_column='USERNAME', unique=True, max_length=250)
    password = models.CharField(
        db_column='PASSWORD', max_length=50, blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=100)
    surname = models.CharField(db_column='SURNAME', max_length=100)
    email = models.CharField(
        db_column='EMAIL', max_length=100, blank=True, null=True)
    phone = models.CharField(
        db_column='PHONE', max_length=100, blank=True, null=True)
    disabled = models.PositiveSmallIntegerField(db_column='DISABLED')
    language = models.CharField(db_column='LANGUAGE', max_length=2)
    last_login = models.DateTimeField(
        db_column='LAST_REQUEST_DATE', blank=True, null=True)
    address = models.CharField(
        db_column='ADDRESS', max_length=100, blank=True, null=True)
    city = models.CharField(
        db_column='CITY', max_length=100, blank=True, null=True)
    zip = models.CharField(
        db_column='ZIP', max_length=10, blank=True, null=True)

    def _make_password(self, raw_password):
        salted = settings.AUTH_PASSWORT_SALT + raw_password
        return hashlib.md5(salted.encode()).hexdigest()

    def set_password(self, raw_password):
        self.password = self._make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        return self.password == self._make_password(raw_password)

    @property
    def is_active(self):
        return not self.disabled

    class Meta:
        managed = True
        db_table = 'USER'


class Group(models.Model):
    group_id = models.AutoField(db_column='GROUP_ID', primary_key=True)
    role = models.ForeignKey('core.Role', models.DO_NOTHING,
                             db_column='ROLE_ID', related_name='+')
    service = models.ForeignKey('core.Service', models.DO_NOTHING,
                                db_column='SERVICE_ID', related_name='+',
                                blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=100)
    phone = models.CharField(
        db_column='PHONE', max_length=100, blank=True, null=True)
    zip = models.CharField(
        db_column='ZIP', max_length=10, blank=True, null=True)
    city = models.CharField(
        db_column='CITY', max_length=100, blank=True, null=True)
    address = models.CharField(
        db_column='ADDRESS', max_length=100, blank=True, null=True)
    email = models.CharField(
        db_column='EMAIL', max_length=100, blank=True, null=True)
    website = models.CharField(
        db_column='WEBSITE', max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'GROUP'


class GroupLocation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    group = models.ForeignKey(Group, models.DO_NOTHING,
                              db_column='GROUP_ID', related_name='+')
    location = models.ForeignKey(
        'core.Location', models.DO_NOTHING, db_column='LOCATION_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'GROUP_LOCATION'
        unique_together = (('group', 'location'),)


class UserGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING,
                             db_column='USER_ID', related_name='user_groups')
    group = models.ForeignKey(Group, models.DO_NOTHING,
                              db_column='GROUP_ID', related_name='+')
    default_group = models.PositiveSmallIntegerField(db_column='DEFAULT_GROUP')

    class Meta:
        managed = True
        db_table = 'USER_GROUP'
        unique_together = (('user', 'group'),)
