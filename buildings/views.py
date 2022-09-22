from django.shortcuts import render
from .models import Buildings, Buildingaccess
from infections.models import Users
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .serializers import BuildingRegisterSerializer
import qrcode
import io
import base64

# Create your views here.

class GenerateQRCodeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            building = Buildings.objects.get(name=kwargs['name'])
        except Buildings.DoesNotExist:
            raise ValidationError(detail="Building does not exist")
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(building.id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        tmp = io.BytesIO()
        img_save = img.save(tmp)
        png_qr = tmp.getvalue()
        b64_img = base64.b64encode(png_qr)
        return Response(data={"qrcode": b64_img}, status=status.HTTP_200_OK)

class BuildingAccessRegister (CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            building = Buildings.objects.get(id=request.data['building'])
        except Buildings.DoesNotExist:
            raise ValidationError(detail="Building does not exist")
        try:
            user = Users.objects.get(id=request.user.id)
        except Users.DoesNotExist:
            raise ValidationError(detail="User does not exist")
        try:
            buildingaccess = Buildingaccess.objects.get(user=user, building=building)
            raise ValidationError(detail="User already accessed this building")
        except Buildingaccess.DoesNotExist:
            request.data['user'] =request.user.id
            buildingaccess = BuildingRegisterSerializer(data=request.data)
            buildingaccess.is_valid(raise_exception=True)
            buildingaccess.save()
        return Response(status=status.HTTP_201_CREATED)