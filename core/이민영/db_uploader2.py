import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shabang.settings")
django.setup()

from room.models         import Room, Image, Agency, Status, FloorType, RoomType, StructureType, Parking, Direction
from apartment.models    import District, Neighborhood, TradeType


# Direction

CSV_PATH_PRODUCTS = './Direction.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]

        Direction.objects.create(name=name)

# Parking
CSV_PATH_PRODUCTS = './Parking.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        count = row[0]

        Parking.objects.create(count=count)

# StructureType
CSV_PATH_PRODUCTS = './StructureType.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]

        StructureType.objects.create(name=name)

# RoomType
CSV_PATH_PRODUCTS = './RoomType.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]

        RoomType.objects.create(name=name)

# FloorType
CSV_PATH_PRODUCTS = './FloorType.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]

        FloorType.objects.create(name=name)

# Status
CSV_PATH_PRODUCTS = './Status.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        status = row[0]

        Status.objects.create(status=status)

# Agency
CSV_PATH_PRODUCTS = './Agency.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name         = row[0]
        phone_number = row[1]
        image_url    = row[2]
        description  = row[3]

        Agency.objects.create(name=name, phone_number=phone_number, image_url=image_url, description=description)

# TradeType
#CSV_PATH_PRODUCTS = './TradeType.csv'
#
#with open(CSV_PATH_PRODUCTS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        name = row[0]
#
#        TradeType.objects.create(name=name)

## Neighborhood
#CSV_PATH_PRODUCTS = './Neighborhood.csv'
#
#with open(CSV_PATH_PRODUCTS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        name = row[0]
#
#        Neighborhood.objects.create(name=name)
#
# District
#CSV_PATH_PRODUCTS = './District.csv'
#
#with open(CSV_PATH_PRODUCTS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        name            = row[0]
#        neighborhood_id = row[1]
#
#        District.objects.create(name=name)
#
# Room
CSV_PATH_PRODUCTS = './Room.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        latitude          = row[0]
        longitude         = row[1]
        register_number   = row[2]
        area              = row[3]
        completion_year   = row[4]
        deposit           = row[5]
        rent              = row[6]
        maintenance_cost  = row[7]
        top_floor         = row[8]
        floor             = row[9]
        description       = row[10]
        address           = row[11]
        available_date    = row[12]
        has_elevator      = row[13]
        trade_type_id     = row[14]
        agency_id         = row[15]
        status_id         = row[16]
        floor_type_id     = row[17]
        room_type_id      = row[18]
        structure_type_id = row[19]
        parking_id        = row[20]
        direction_id      = row[21]

        Room.objects.create(
            latitude=latitude,
            longitude=longitude,
            register_number=register_number,
            area=area,
            completion_year=completion_year,
            deposit=deposit,
            rent=rent,
            maintenance_cost=maintenance_cost,
            top_floor=top_floor,
            floor=floor,
            description=description,
            address=address,
            available_date=available_date,
            has_elevator=has_elevator,
            trade_type_id=trade_type_id,
            agency_id=agency_id,
            status_id=status_id,
            floor_type_id=floor_type_id,
            room_type_id=room_type_id,
            structure_type_id=structure_type_id,
            parking_id=parking_id,
            direction_id=direction_id
            )

# Image
CSV_PATH_PRODUCTS = './Image.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        image_url = row[0]
        room_id   = row[1]

        Image.objects.create(image_url=image_url, room_id=room_id)
