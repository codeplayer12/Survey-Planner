from django.contrib import admin

# Register your models here.
from .models import Camera, SurveyType

admin.site.register(Camera)
admin.site.register(SurveyType)
