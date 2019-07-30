from django_filters.rest_framework import FilterSet

from . import models


class ApplicantFilterSet(FilterSet):
    class Meta:
        model = models.Applicant
        fields = ("instance",)
