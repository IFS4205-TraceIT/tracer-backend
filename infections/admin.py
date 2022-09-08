from django.contrib import admin

from .models import (
    User,
    Closecontacts,
    Infectionhistory,
    Notifications,
    Contacttracers
)
# Register your models here.
@admin.register(User,Closecontacts,Infectionhistory,Notifications,Contacttracers)
class InfectionAdmin(admin.ModelAdmin):
    pass