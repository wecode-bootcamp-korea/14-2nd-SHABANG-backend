from django.db import models

from core      import models as core_models

class Apartment(core_models.TimeStampModel):
    price             = models.DecimalField(max_digits=20, decimal_places=4)
    top_floor         = models.IntegerField()
    floor             = models.IntegerField()
    trade_year        = models.IntegerField()
    trade_month       = models.IntegerField()
    apartment_complex = models.ForeignKey('ApartmentComplex', on_delete=models.CASCADE)
    neighborhood      = models.ForeignKey('Neighborhood', on_delete=models.SET_NULL, null=True)
    district          = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)
    neighborhood      = models.ForeignKey('Neighborhood', on_delete=models.SET_NULL, null=True)
    trade_type        = models.ForeignKey('TradeType', on_delete=models.SET_NULL, null=True)
    size              = models.ForeignKey('Size', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'apartments'

class ApartmentComplex(models.Model):
    name             = models.CharField(max_length=100)
    household_number = models.IntegerField()
    completion_year  = models.CharField(max_length=20)
    image_url        = models.URLField(max_length=1000, null=True)
    address          = models.CharField(max_length=1000)
    longitude        = models.DecimalField(max_digits=20, decimal_places=15)
    latitude         = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'complexes'

    def __str__(self):
        return self.name

class District(models.Model):
    name      = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'districts'

    def __str__(self):
        return self.name

class Neighborhood(models.Model):
    name      = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)
    district  = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'neighborhoods'
    def __str__(self):
        return self.name

class TradeType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'trade_types'

    def __str__(self):
        return self.name

class Size(models.Model):
    area = models.IntegerField()

    class Meta:
        db_table = 'sizes'
