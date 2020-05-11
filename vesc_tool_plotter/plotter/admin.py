from django.contrib import admin

# Register your models here.
from .models import Ride, Build

admin.site.register(Ride)
admin.site.register(Build)
