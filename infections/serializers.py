from .models import (
    User, 
    Closecontacts, 
    Infectionhistory,
    Notifications
    )
from rest_framework import exceptions, serializers 
from datetime import date, timedelta

class UserNotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = '__all__'

class ListInfectedSerializer (serializers.ModelSerializer):
    infected = serializers.BooleanField(default=True)
    infected_time = serializers.SlugRelatedField(source="infectionhistory", read_only=True, slug_field='recorded_timestamp')
    notifications_set = UserNotificationsSerializer(many = True, read_only= True)
    class Meta:
        model = User
        fields = (
            'id',
            'nric',
            'name',
            'email',
            'phone',
            'infected_time',
            'infected',
            'notifications_set'
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
