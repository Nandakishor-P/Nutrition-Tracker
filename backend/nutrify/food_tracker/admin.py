from django.contrib import admin
from .models import FoodLog, WaterLog, Goal

admin.site.register(FoodLog)
admin.site.register(WaterLog)
admin.site.register(Goal)
