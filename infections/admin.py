from django.contrib import admin

from .models import (
    UserInfo,
    Closecontacts,
    Infectionhistory,
    Notifications,
    Contacttracers
)
# Register your models here.
@admin.register(UserInfo,Closecontacts,Infectionhistory,Notifications,Contacttracers)
class InfectionAdmin(admin.ModelAdmin):
    pass