#!/usr/bin/env python3

# This file will contain custom validations for CALUMA-BE.
#
# Currently, this is only a sketch of what needs to be done, and is only here
# so it doesn't get forgotten.

from caluma.core.validations import BaseValidation, validation_for
from caluma.form.schema import SaveDocumentAnswer


class CustomValidation(BaseValidation):
    @validation_for(SaveDocumentAnswer)
    def validate_answer_mutation(self, mutation, data, info):
        # TODO (validation SaveAnswer mutation): check if "gesuchsteller" email
        # question. If yes, validate email exists in NG user database
        return data
