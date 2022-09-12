from django.urls import path

from .views import (
    ListInfectionAPIView,
    ListCloseContactAPIView,
    UpdateUploadStatusAPIView
)

app_name = 'infections'

urlpatterns = [
    path('infections', ListInfectionAPIView.as_view()),
    path('infections/<date>', ListInfectionAPIView.as_view()),
    path('closecontacts/<infectedId>',ListCloseContactAPIView.as_view()),
    path('notify/<pk>', UpdateUploadStatusAPIView.as_view())
]