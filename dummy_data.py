import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from faker import Faker
import random
from products.models import Product, Brand, ProductImages, Review
from django.contrib.auth.models import User


def seed_brand(n):
    fake = Faker()

    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']

    for _ in range(n):
        Brand.objects.create(
            name=fake.name(),
            image=f"brand/{images[random.randint(0, 9)]}"
        )


def seed_product(n):
    fake = Faker()

    flag_types = ['NEW', 'FEATURE', 'SALE']

    brands = Brand.objects.all()

    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']

    for _ in range(n):
        Product.objects.create(
            name=fake.name(),
            flag=random.choice(flag_types),
            price=round(random.uniform(1.99, 99.99), 2),
            image=f"product/{images[random.randint(0, 9)]}",
            sku=random.randint(10000, 99999),
            subtitle=fake.text(max_nb_chars=450),
            description=fake.text(max_nb_chars=3000),
            brand=brands[random.randint(0, len(brands) - 1)]
        )


def seed_users(n):
    fake = Faker()

    for _ in range(n):
        User.objects.create(
            username=fake.user_name(),
            password='MoH.1822'
        )


def seed_reviews(n):
    fake = Faker()

    users = User.objects.all()

    products = Product.objects.all()

    for _ in range(n):
        Review.objects.create(
            user=users[random.randint(0, len(users) - 1)],
            product=products[random.randint(0, len(products) - 1)],
            review=fake.text(max_nb_chars=500),
            rate=random.randint(1, 5),
            created_at=fake.date_time_this_year(),
        )


seed_reviews(500)