import itertools
import json
import os
import sys

import inflection
from django.conf import settings
from django.utils.translation import gettext as _
from pyjexl.jexl import JEXL
from rest_framework import exceptions

from camac.document.models import Attachment

from . import models


class FormDataValidator(object):
    def __init__(self, instance):
        self.forms_def = json.loads(
            settings.APPLICATION_DIR.file('form.json').read()
        )
        self.instance = instance
        self.fields = {
            **{
                field.name: field.value
                for field in models.FormField.objects.filter(instance=instance)
            },
            # handle attachments like fields
            **{
                os.path.splitext(attachment.name)[0]: attachment.path
                for attachment in Attachment.objects.filter(instance=instance)
            }
        }
        self.jexl = JEXL()
        self.jexl.add_transform(
            'value',
            lambda name: self.fields.get(name)
        )

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

    def _validate_question_document(self, question, question_def, value):
        if not value:
            raise exceptions.ValidationError(
                _('Document missing for question `%(field)s') % {
                    'field': question
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

        expression = question_def.get('active-expression', None)

        try:
            return expression is None or self.jexl.evaluate(expression)
        except TypeError:
            # A TypeError is raised if a question is not filled. It then tries
            # to e.g compare None < 250 which can't work
            return False

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
