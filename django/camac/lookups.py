from django.db.models import Lookup


class Any(Lookup):
    """
    Check if element is present in ArrayField.

    Using element = ANY(array) operator, requires lhs and rhs of expression to be of same type.
    This is a replacement for Func(*args, function="ANY").
    See linked issue for more details:
    https://code.djangoproject.com/ticket/34079
    """

    lookup_name = "any"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = (*lhs_params, *rhs_params)
        return f"{lhs} = ANY({rhs})", params
