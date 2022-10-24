from .models import (
    Users, 
    Closecontacts, 
    Infectionhistory,
    Notifications
    )
from django.utils import timezone
from rest_framework import exceptions, serializers 
from datetime import date, timedelta

class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = '__all__'

class InfectionHistorySerializer(serializers.ModelSerializer):
    notifications = NotificationsSerializer()
    class Meta:
        model = Infectionhistory
        exclude = ('user',)
        depth = 2

class ListInfectedSerializer (serializers.ModelSerializer):
    infections = InfectionHistorySerializer(required=False)
    class Meta:
        model = Users
        fields = (
            'id',
            'nric',

            'name',
            'email',
            'phone',
            'infections'
            )

class CloseContactsSerializer (serializers.ModelSerializer):
    uid = serializers.UUIDField(source="contacted_user.id", read_only=True)
    name = serializers.CharField(source="contacted_user.name", read_only=True)
    phone = serializers.IntegerField(source="contacted_user.phone", read_only=True)
    email = serializers.CharField(source="contacted_user.email", read_only=True)
    gender = serializers.CharField(source="contacted_user.gender", read_only=True)
    nric = serializers.CharField(source="contacted_user.nric", read_only=True)

    class Meta:
        model = Closecontacts
        fields = (
            'infected_user',
            'contact_timestamp',
            'uid',
            'name',
            'phone',
            'email',
            'gender',
            'nric'
        )

class UpdateUploadSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(default=timezone.now().date()+timedelta(days=7))
    start_date = serializers.DateField(default=timezone.now().date())

    class Meta:
        model = Notifications
        fields = '__all__'
