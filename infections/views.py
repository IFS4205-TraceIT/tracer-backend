from django.shortcuts import render
from .models import Users, Notifications
from .serializers import (
    ListInfectedSerializer, 
    CloseContactsSerializer,
    UpdateUploadSerializer
)
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from datetime import date, timedelta, datetime
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated

#Remove later once auth and jwt is done
import uuid


class ListInfectionAPIView(ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = ListInfectedSerializer
    model = serializer_class.Meta.model
    lookup_url_kwarg = "date"

    def get_queryset(self):
        querydate = self.kwargs.get(self.lookup_url_kwarg, None)
        if querydate is None:
            querydate = date.today()
        else:
            try:
                querydate =  datetime.strptime(querydate,"%Y-%m-%d")
            except ValueError:
                raise ValidationError(detail="Invalid Date format, yyyy-mm-dd")

        querydate = querydate + timedelta(days=1)
        queryset = self.model.objects.all() 
        for user in queryset:
            infectedhistory = user.infectionhistory_set.filter(
                recorded_timestamp__range=(
                    querydate-timedelta(days=15),
                    querydate
                    ))
            if len(infectedhistory) > 0:
                user.infections = infectedhistory.latest("recorded_timestamp")
            else:
                user.infected = False
            
        return queryset

class ListCloseContactAPIView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CloseContactsSerializer
    model = serializer_class.Meta.model
    lookup_url_kwarg = "infectedId"

    def get_queryset(self):

        uid = self.kwargs.get(self.lookup_url_kwarg)
        closeContact = self.model.objects.filter(infected_user=uid)
        return closeContact

class UpdateUploadStatusAPIView(UpdateAPIView): 

    permission_classes = (IsAuthenticated,)
    queryset = Notifications.objects.all()
    serializer_class = UpdateUploadSerializer

    def get_object(self, pk):
        try:
            cur_infection = Users.objects.get(id=pk).infectionhistory_set.latest("recorded_timestamp")
        except:
            raise ValidationError(detail="Invalid User!")

        try:
            return self.get_queryset().get(infection = cur_infection), cur_infection
        except Notifications.DoesNotExist:
            return None, cur_infection

    def update(self, request, pk):

        contact_tracer_id = request.user.id
        cur_notification, infection_id =  self.get_object(pk)

        if cur_notification is None:
            serial = self.serializer_class(data={
                'infection': infection_id.id,
                'tracer':contact_tracer_id,     
                'uploaded_status': False
            })
            serial.is_valid(raise_exception=True)
            serial.save()
        else:
            serial = self.serializer_class(cur_notification, data = {'uploaded_status': False}, partial=True)
            serial.is_valid(raise_exception=True)
            serial.save()

        return Response(status=status.HTTP_200_OK)

        