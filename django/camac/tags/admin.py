from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, display, register
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.django_admin.utils import display_color

from .models import InstanceMark


@register(InstanceMark)
class InstanceMarkAdmin(
    EbauAdminMixin, SortableAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin
):
    list_display = ["sort", "name", "icon", "background_color_box", "text_color_box"]
    exclude = ["instance"]

    @display(description="Background color")
    def background_color_box(self, obj):
        return display_color(obj.background_color)

    @display(description="Text color")
    def text_color_box(self, obj):
        return display_color(obj.text_color)
