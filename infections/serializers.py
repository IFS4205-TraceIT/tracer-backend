from .models import (
    User, 
    Closecontacts, 
    Infectionhistory,
    Notifications
    )
from rest_framework import exceptions, serializers 
from datetime import date, timedelta

class ListInfectedSerializer (serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(source="infectionhistory.recorded_timestamp")
    infected = serializers.BooleanField(default=True)
    infected_time = serializers.SlugRelatedField(source="infectionhistory", read_only=True, slug_field='recorded_timestamp')
    class Meta:
        model = User
        fields = (
            'id',
            'nric',
            'name',
            'email',
            'phone',
            'timestamp',
            'infected_time',
            'infected',
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
