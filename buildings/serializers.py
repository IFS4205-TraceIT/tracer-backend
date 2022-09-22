from .models import Buildings,Buildingaccess
from rest_framework import serializers 
from datetime import date

class BuildingRegisterSerializer(serializers.ModelSerializer):
    access_timestamp = serializers.DateTimeField(default=date.today())
    class Meta:
        model = Buildingaccess
        fields = '__all__'