from django.db import models
from infections.models import Users

# Create your models here.
class Buildingaccess(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    building = models.ForeignKey('Buildings', on_delete=models.CASCADE)
    access_timestamp = models.DateTimeField()

    class Meta:
        db_table = 'buildingaccess'
        unique_together = (('user', 'building', 'access_timestamp'),)


class Buildings(models.Model):
    name = models.TextField()
    location = models.IntegerField()

    class Meta:
        db_table = 'buildings'