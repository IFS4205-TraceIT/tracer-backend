from .models import Buildings,Buildingaccess
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from datetime import date, timedelta, datetime
from .serializers import BuildingSerializer, BuildingAccessSerializer


# Create your views here.

class ListBuilding (ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BuildingSerializer
    queryset = Buildings.objects.all()

class ListBuildingAccess (ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BuildingAccessSerializer
    lookup_url_kwarg = ["buildingid","date"]

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg[0])
        querydate = self.kwargs.get(self.lookup_url_kwarg[1], None)
        if querydate is None:
            querydate = datetime.combine(date.today(), datetime.min.time())
        else:
            try:
                querydate =  datetime.strptime(querydate,"%Y-%m-%d")
            except ValueError:
                raise ValidationError(detail="Invalid Date format, yyyy-mm-dd")
        try:
            building = Buildings.objects.get(id = id)
        except Buildings.DoesNotExist:
            raise ValidationError(detail="Invalid Building!")

        result = Buildingaccess.objects.filter(building = building, access_timestamp__range=(querydate,querydate+timedelta(hours=23,minutes=59)))
        return result