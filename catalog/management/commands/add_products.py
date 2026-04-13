from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add product to the database"

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Category.objects.all().delete()
        Product.objects.all().delete()
        category, _ = Category.objects.get_or_create(
            name="Овощи", description="Свежие овощи"
        )

        products = [
            {
                "name": "Огурец",
                "description": "Не фрукт",
                "price": "50",
                "category": category,
            },
            {
                "name": "Помидор",
                "description": "Овощ",
                "price": "50",
                "category": category,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product already exist: {product.name}")
                )
