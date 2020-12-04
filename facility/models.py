from django.db import models

class School(models.Model):
    name         = models.CharField(max_length=200)
    longitude    = models.DecimalField(max_digits=20, decimal_places=15)
    latitude     = models.DecimalField(max_digits=20, decimal_places=15)
    school_grade = models.ForeignKey('SchoolGrade', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'schools'

    def __str__(self):
        return self.name

class SchoolGrade(models.Model):
    grade = models.CharField(max_length=20)

    class Meta:
        db_table = 'school_grades'

    def __str__(self):
        return self.grade

class Subway(models.Model):
    name        = models.CharField(max_length=20)
    longitude   = models.DecimalField(max_digits=20, decimal_places=15)
    latitude    = models.DecimalField(max_digits=20, decimal_places=15)
    subway_line = models.ForeignKey('SubwayLine', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'subways'

    def __str__(self):
        return self.name

class SubwayLine(models.Model):
    line = models.CharField(max_length=20)

    class Meta:
        db_table = 'subway_lines'

    def __str__(self):
        return self.line

class ConvenientStore(models.Model):
    name      = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'convenient_stores'

    def __str__(self):
        return self.name

class Cafe(models.Model):
    name      = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    latitude  = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        db_table = 'cafes'

    def __str__(self):
        return self.name
