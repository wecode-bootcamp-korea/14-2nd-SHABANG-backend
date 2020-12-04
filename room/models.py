from django.db import models

from core      import models as core_models

class Room(core_models.TimeStampModel):
    longitude        = models.DecimalField(max_digits=20, decimal_places=15)
    latitude         = models.DecimalField(max_digits=20, decimal_places=15)
    register_number  = models.IntegerField()
    area             = models.DecimalField(max_digits=10, decimal_places=5)
    completion_year  = models.CharField(max_length=20)
    deposit          = models.DecimalField(max_digits=20, decimal_places=4)
    rent             = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    maintenance_cost = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    top_floor        = models.IntegerField()
    floor            = models.IntegerField()
    description      = models.TextField(null=True)
    address          = models.CharField(max_length=1000)
    available_date   = models.CharField(max_length=100, null=True)
    trade_date       = models.DateTimeField(null=True)
    trade_type       = models.ForeignKey('apartment.TradeType', on_delete=models.SET_NULL, null=True)
    agency           = models.ForeignKey('Agency', on_delete=models.CASCADE)
    status           = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    floor_type       = models.ForeignKey('FloorType', on_delete=models.SET_NULL, null=True)
    room_type        = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True)
    structure_type   = models.ForeignKey('StructureType', on_delete=models.SET_NULL, null=True)
    parking          = models.ForeignKey('Parking', on_delete=models.SET_NULL, null=True)
    direction        = models.ForeignKey('Direction', on_delete=models.SET_NULL, null=True)
    has_elevator     = models.BooleanField()

    class Meta:
        db_table = 'rooms'

class Image(models.Model):
    image_url = models.URLField(max_length=1000)
    room      = models.ForeignKey('Room', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

class Agency(models.Model):
    name         = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True)
    image_url    = models.URLField(max_length=1000, null=True)
    description  = models.TextField(null=True)

    class Meta:
        db_table = 'agencies'

    def __str__(self):
        return self.name

class Status(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'status'

    def __str__(self):
        return self.status

class FloorType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'floor_types'

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'room_types'

    def __str__(self):
        return self.name

class StructureType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'structure_types'

    def __str__(self):
        return self.name

class Parking(models.Model):
    count = models.CharField(max_length=20)

    class Meta:
        db_table = 'parkings'

    def __str__(self):
        return self.count

class Direction(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'directions'

    def __str__(self):
        return self.name
