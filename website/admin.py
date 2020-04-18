from django.contrib import admin

# Register your models here.
from .models import Waypoints,Distance

admin.site.register(Waypoints)
admin.site.register(Distance)