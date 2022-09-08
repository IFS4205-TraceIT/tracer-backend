import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True)
    nric = models.TextField(unique=True)
    name = models.TextField()
    dob = models.DateField()
    email = models.TextField(blank=True, null=True)
    phone = models.IntegerField()
    gender = models.CharField(max_length=1)
    address = models.TextField()
    zip_code = models.IntegerField()

    class Meta:
        db_table = 'userinfo'


class Infectionhistory(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    recorded_timestamp = models.DateTimeField()

    class Meta:
        db_table = 'infectionhistory'
        unique_together = (('user', 'recorded_timestamp'),)


class Closecontacts(models.Model):
    infected_user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True, related_name="infected_user")
    contacted_user = models.ForeignKey(User, models.DO_NOTHING, related_name="contacted_user")
    contact_timestamp = models.DateTimeField()
    rssi = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        db_table = 'closecontacts'
        unique_together = (('infected_user', 'contacted_user', 'contact_timestamp'),)

class Contacttracers(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        db_table = 'contacttracers'

class Notifications(models.Model):
    due_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    tracer = models.ForeignKey(Contacttracers, models.DO_NOTHING, blank=True, null=True)
    infected_user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'