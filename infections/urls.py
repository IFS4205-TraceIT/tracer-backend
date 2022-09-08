from django.urls import path

from .views import (
    ListInfectionAPIView,
    ListCloseContactAPIView,
    UpdateUploadStatusAPIView
)

app_name = 'infections'

urlpatterns = [
    path('infections', ListInfectionAPIView.as_view(), name='list_infections'),
    path('closecontacts/<infectedId>',ListCloseContactAPIView.as_view(),name='list_closecontacts'),
    path('notify/<pk>', UpdateUploadStatusAPIView.as_view())
]