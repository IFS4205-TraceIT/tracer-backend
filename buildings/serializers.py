from .models import Buildings,Buildingaccess
from infections.models import Users
from rest_framework import serializers 
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name','nric','gender','email','phone']

class BuildingAccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Buildingaccess
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buildings
        fields = '__all__'

