from alexandria.core.models import Category
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Apply Alexandria permissions config to the database"

    def handle(self, *args, **kwargs):
        permissions_config = settings.ALEXANDRIA.get("PERMISSIONS_CONFIG")
        if not permissions_config:
            self.stdout.write(
                self.style.ERROR("Permissions config is not set in settings.")
            )
            return

        for category_name, permission_info in permissions_config.items():
            try:
                category = Category.objects.get(pk=category_name)
                category.metainfo = {"access": permission_info}
                category.save()
                self.stdout.write(f"Updated category: {category_name}")
            except Category.DoesNotExist:
                self.stdout.write(f"Category does not exist: {category_name}")

        self.stdout.write(
            self.style.SUCCESS("Permissions config applied successfully.")
        )
