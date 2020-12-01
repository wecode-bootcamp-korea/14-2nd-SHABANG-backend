from django.db import models

class School(models.Model):
    name      = models.CharField(max_length=200)
    grade     = models.CharField(max_length=20)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'schools'

    def __str__(self):
        return self.name

class Subway(models.Model):
    name      = models.CharField(max_length=20)
    line      = models.CharField(max_length=20)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'subways'

    def __str__(self):
        return self.name

class ConvenientStore(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'convenient_stores'

class Cafe(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'cafes'
