from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from alexandria.core.models import BaseModel, Document, File, Category, Tag


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        if request.user.role == "support":
            return queryset

        return queryset.none() 

    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, queryset, request):
        return queryset

    @filter_queryset_for(File)
    def filter_queryset_for_file(self, queryset, request):
        # Limitations for `Document` should also be enforced on `File`.
        return queryset

    @filter_queryset_for(Category)
    def filter_queryset_for_category(self, queryset, request):
        return queryset
    
    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        return queryset
