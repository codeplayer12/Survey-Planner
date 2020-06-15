from django.contrib import admin

# Register your models here.
from .models import Camera, SurveyType,Drone,BudgetItem

admin.site.register(Camera)
admin.site.register(SurveyType)
admin.site.register(Drone)
admin.site.register(BudgetItem)
