import itertools
import json
import sys

import inflection
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import exceptions

from . import models


class FormDataValidator(object):
    def __init__(self, instance):
        self.forms_def = json.loads(
            settings.APPLICATION_DIR.file('form.json').read()
        )
        self.instance = instance
        self.fields = {
            field.name: field.value
            for field in models.FormField.objects.filter(instance=instance)
        }

    def _validate_question_select(self, question, question_def, value):
        self._validate_question_radio(question, question_def, value)

    def _validate_question_radio(self, question, question_def, value):
        if value not in question_def['config']['options']:
            raise exceptions.ValidationError(
                _('Invalid value `%(value)s` in field `%(field)s`') % {
                    'value': value,
                    'field': question
                }
            )

    def _validate_question_checkbox(self, question, question_def, value):
        options = set(question_def['config']['options'])
        # avoid `TypeError` as value may be None

        values = set(value or [None])
        diff = values - options

        if diff:
            raise exceptions.ValidationError(
                _('Invalid values `%(values)s` in field `%(field)s`') % {
                    'values': ', '.join([str(val) for val in diff]),
                    'field': question
                }
            )

    def _validate_question_multiselect(self, question, question_def, value):
        options = set(question_def['config']['options'])
        allow_custom = question_def['config'].get('allow-custom')
        # avoid `TypeError` as value may be None
        values = set(value or [None])
        diff = values - options

        if diff and not allow_custom:
            raise exceptions.ValidationError(
                _('Invalid values `%(values)s` in field `%(field)s`') % {
                    'values': ', '.join([str(val) for val in diff]),
                    'field': question
                }
            )

    def _validate_question_text(self, question, question_def, value):
        if not isinstance(value, str) or not value:
            raise exceptions.ValidationError(
                _('Value of field `%(field)s` must be `str` and not empty') % {
                    'field': question
                }
            )

    def _validate_question_number(self, question, question_def, value):
        min_val = question_def['config'].get('min', -sys.maxsize - 1)
        max_val = question_def['config'].get('max', sys.maxsize)

        if (
            not isinstance(value, int) and not isinstance(value, float) or
            value < min_val or
            value > max_val
        ):
            raise exceptions.ValidationError(
                _('Value of field `%(field)s` needs to be a number '
                  'between %(min_val)s and %(max_val)s).') % {
                      'field': question,
                      'min_val': min_val,
                      'max_val': max_val
                }
            )

    def _validate_question_gwr(self, question, question_def, value):
        # TODO: might be better generic table with a gwr config option
        self._validate_question_table(question, question_def, value)

    def _validate_question_table(self, question, question_def, value):
        columns = question_def['config']['columns']
        for row in list(value or [{}]):
            for column in columns:
                self._validate_question(
                    '{0}/{1}'.format(question, column['name']),
                    column,
                    row.get(column['name'])
                )

    def _check_question_required(self, question, question_def):
        if not question_def['required']:
            return False

        # only required when all active conditions are met
        for cond in question_def.get('active-condition', []):
            value = self.fields.get(cond['question'])
            if not isinstance(value, list):
                # avoid single values
                value = [value]

            for condition_type, condition_values in cond['value'].items():
                condition_check_method = getattr(
                    self,
                    '_check_active_condition_{0}'.format(
                        inflection.underscore(condition_type)
                    )
                )

                if not condition_check_method(value, condition_values):
                    return False

        return True

    def _check_active_condition_contains_any(self, value, condition_values):
        return not set(value) & set(condition_values)

    def _check_active_condition_contains_not_any(
        self, value, condition_values
    ):
        return set(value) & set(condition_values)

    def _validate_question(self, question, question_def, value):
        required = self._check_question_required(question, question_def)

        # do not validate optional fields without a value
        if not required and not value:
            return

        validate_method = getattr(
            self,
            '_validate_question_{0}'.format(
                inflection.underscore(question_def['type'])
            )
        )
        validate_method(question, question_def, value)

    def validate(self):
        form_def = self.forms_def['forms'].get(self.instance.form.name)

        if form_def is None:
            raise exceptions.ValidationError(
                _('Invalid form type %(form)s.') % {
                    'form': self.instance.form.name
                }
            )

        questions = itertools.chain(*[
            self.forms_def['modules'][module]['questions']
            for module in form_def
        ])

        for question in questions:
            value = self.fields.get(question)
            self._validate_question(
                question, self.forms_def['questions'][question], value
            )
