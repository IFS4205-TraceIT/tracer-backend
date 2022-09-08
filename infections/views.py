from django.shortcuts import render
from .models import User, Notifications
from .serializers import (
    ListInfectedSerializer, 
    CloseContactsSerializer,
    UpdateUploadSerializer
)
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from datetime import date, timedelta
from rest_framework import status
from django.http import Http404

#Remove later once auth and jwt is done
import uuid


class ListInfectionAPIView(ListAPIView):
    serializer_class = ListInfectedSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset = self.model.objects.filter(infectionhistory__recorded_timestamp__gte=date.today()-timedelta(days=14))
        return queryset

class ListCloseContactAPIView(ListAPIView):
    serializer_class = CloseContactsSerializer
    model = serializer_class.Meta.model
    lookup_url_kwarg = "infectedId"

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        closeContact = self.model.objects.filter(infected_user=uid)
        return closeContact

class UpdateUploadStatusAPIView(UpdateAPIView): 
    queryset = Notifications.objects.all()
    serializer_class = UpdateUploadSerializer

    def get_object(self, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            raise Http404
        try:
            return self.get_queryset().get(infected_user=user) 
        except Notifications.DoesNotExist:
            return None

    def update(self, request, pk):
        contact_tracer_id = uuid.UUID("63a4d5b9-b061-4e30-9328-aabfaf865b02")
        cur_notification =  self.get_object(pk)
        print(cur_notification)
        if cur_notification is None:
            print("No object creating notification")
            serial = self.serializer_class(data= {
                'infected_user': uuid.UUID(pk),
                'tracer':contact_tracer_id,     
                'status': True
            })
            serial.is_valid(raise_exception=True)
            serial.save()
        else:
            serial = self.serializer_class(cur_notification, data = {'status': True}, partial=True)
            serial.is_valid(raise_exception=True)
            serial.save()

        return Response(status=status.HTTP_200_OK)

        
