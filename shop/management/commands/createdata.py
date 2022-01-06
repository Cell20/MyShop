from django.core.management.base import BaseCommand
from faker import Faker
# pip install Faker
import faker.providers
from shop.models import Category, Product
import random
from decouple import config
from django.contrib.auth.models import User
# import urllib.request
# from datetime import date
# import os


CATEGORIES = [
    "Shoes",
    "Boots",
    "Trainers",
    "Clothes",
    "Dress",
    "T-shirt",
    "Jeans",
    "Shirts",
    "PrintedShirts",
    "TankTops",
    "PoloShirt",
    "Beauty",
    "DIYTools",
    "GardenOutdoors",
    "Grocery",
    "HealthPersonalCare",
    "Lighting",
]

PRODUCTS = [
    "Shoes",
    "Boots",
    "Trainers",
    "Clothes",
    "Dress",
    "T-shirt",
    "Jeans",
    "Shirts",
    "PrintedShirts",
    "TankTops",
    "PoloShirt",
    "Beauty",
    "DIYTools",
    "GardenOutdoors",
    "Grocery",
    "HealthPersonalCare",
    "Lighting",
]


class Provider(faker.providers.BaseProvider):
    """Class to provide you custom tags, posts, status or anything custom."""

    def ms_category(self):
        return self.random_element(CATEGORIES)

    def ms_products(self):
        return self.random_element(PRODUCTS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) != 1:
            superuser = User.objects.create_superuser(
                username='suhail',
                email=config("EMAIL"),
                password=config("PASSWORD")
            )

        for _ in range(15):
            c = fake.unique.ms_category()
            category = Category.objects.create(name=c, slug=c)

            product = fake.unique.ms_products()
            des = fake.text(max_nb_chars=150)
            price = round(random.uniform(50.99, 99.99), 2)
            Product.objects.create(category=category,
                                   name=product, slug=product, description=des, price=price, available=True
                                   )
