from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов"'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type,
        )

        can_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        group, _ = Group.objects.get_or_create(name='Модератор продуктов')
        group.permissions.add(can_unpublish, can_delete)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))