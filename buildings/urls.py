from django.urls import path

from .views import (
    GenerateQRCodeView,
    BuildingAccessRegister
)

app_name = 'infections'

urlpatterns = [
    path('genqrcode/<name>', GenerateQRCodeView.as_view()),
    path('register', BuildingAccessRegister.as_view()),
]