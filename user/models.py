from django.db import models

from core      import models as core_models

class User(core_models.TimeStampModel):
    name         = models.CharField(max_length=100)
    email        = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

class Favor(core_models.TimeStampModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE)

    class Meta:
        db_table = 'favors'
