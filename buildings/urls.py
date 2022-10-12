from django.urls import path

from .views import (
    ListBuilding,
    ListBuildingAccess,
    ListBuildingUserAccess
)

app_name = 'building'

urlpatterns = [
    path('', ListBuilding.as_view()),
    path('buildingaccess', ListBuildingUserAccess.as_view()),
    path('buildingaccess/<userid>', ListBuildingUserAccess.as_view()),
    path('buildingaccess/<userid>/<date>', ListBuildingUserAccess.as_view()),
    path('<buildingid>', ListBuildingAccess.as_view()),
    path('<buildingid>/<date>', ListBuildingAccess.as_view())
]