from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from alexandria.core.models import BaseModel, Document, File


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        print(request.user)
        import logging
        logging.error(request)
        logging.error(vars(request.user))
        logging.error(queryset)
        return queryset
        return queryset.none()

    """
    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, queryset, request):
        return queryset
        return queryset.exclude(category__slug="protected-category")

    @filter_queryset_for(File)
    def filter_queryset_for_file(self, queryset, request):
        return queryset
        # Limitations for `Document` should also be enforced on `File`.
        return queryset.exclude(document__category__slug="protected-category")
    """
