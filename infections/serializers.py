from .models import (
    Users, 
    Closecontacts, 
    Infectionhistory,
    Notifications
    )
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
    infected = serializers.BooleanField(default=True)
    infections = InfectionHistorySerializer(required=False)
    class Meta:
        model = Users
        fields = (
            'id',
            'nric',
            'name',
            'email',
            'phone',
            'infected',
            'infections'
            )

class CloseContactsSerializer (serializers.ModelSerializer):
    contacted_uid = serializers.UUIDField(source="contacted_user.id", read_only=True)
    contacted_name = serializers.CharField(source="contacted_user.name", read_only=True)
    contacted_phone = serializers.IntegerField(source="contacted_user.phone", read_only=True)
    contacted_email = serializers.CharField(source="contacted_user.email", read_only=True)
    contacted_gender = serializers.CharField(source="contacted_user.gender", read_only=True)

    class Meta:
        model = Closecontacts
        fields = (
            'infected_user',
            'contact_timestamp',
            'contacted_uid',
            'contacted_name',
            'contacted_phone',
            'contacted_email',
            'contacted_gender'
        )
class UpdateUploadSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(default=date.today()+timedelta(days=7))
    start_date = serializers.DateField(default=date.today())

    class Meta:
        model = Notifications
        fields = '__all__'
