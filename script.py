import os
import django

# Correctly set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from products.models import Product
from products.documents import ProductDocument  # Ensure this import works
from decimal import Decimal
import csv

def import_products(csv_file_path):
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            products = []
            for row in reader:
                try:
                    price = Decimal(row['price'].replace(',', '').strip())
                    product = Product(
                        product_name=row['product_name'].strip(),
                        brand=row['brand'].strip(),
                        price=price,
                    )
                    products.append(product)
                except Exception as e:
                    print(f"Error creating product {row.get('product_name', 'Unknown')}: {e}")

            Product.objects.bulk_create(products)
            print(f"Imported {len(products)} products into the database.")

            # Index the products in Elasticsearch
            for product in products:
                ProductDocument().update(product)
            print(f"Indexed {len(products)} products into Elasticsearch.")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "myproject", "data", "MOCK_DATA.csv")
    import_products(csv_file_path)
    print("Data import and indexing completed.")
