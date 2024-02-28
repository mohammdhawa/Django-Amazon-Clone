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


seed_brand(200)