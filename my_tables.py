import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shabang.settings")
django.setup()

from apartment.models import ApartmentComplex, Size, Neighborhood, District, TradeType, Apartment
from user.models      import Platform

CSV_PATH_PRODUCTS = 'complex.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)

    for row in data_reader:
        ApartmentComplex.objects.create(
            name=row[0],
            household_number=row[1],
            completion_year=row[2],
            image_url=row[3],
            address=row[4],
            longitude=row[5],
            latitude=row[6]
        )

CSV_PATH_PRODUCTS = 'size.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Size.objects.create(
            area=row[0]
        )

CSV_PATH_PRODUCTS = 'district.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        District.objects.create(
            name=row[0],
            latitude=row[1],
            longitude=row[2]
        )
CSV_PATH_PRODUCTS = 'neighborhood.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Neighborhood.objects.create(
            name=row[0],
            latitude=row[1],
            longitude=row[2],
            district_id=row[3]
        )

CSV_PATH_PRODUCTS = 'trade_type.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        TradeType.objects.create(
            name=row[0]
        )

CSV_PATH_PRODUCTS = 'apartment.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Apartment.objects.create(
            price=row[0],
            top_floor=row[1],
            floor=row[2],
            apartment_complex_id=row[3],
            neighborhood_id=row[4],
            trade_type_id=row[5],
            trade_month=row[6],
            trade_year=row[7],
            size_id=row[8]
        )
CSV_PATH_PRODUCTS = 'platform.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Platform.objects.create(
            name=row[0]
        )
