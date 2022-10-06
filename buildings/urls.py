from django.urls import path

from .views import (
    ListBuilding,
    ListBuildingAccess
)

app_name = 'building'

urlpatterns = [
    path('', ListBuilding.as_view()),
    path('<buildingid>', ListBuildingAccess.as_view()),
    path('<buildingid>/<date>', ListBuildingAccess.as_view()),
]