from django.contrib import admin

# Register your models here.
from .models import Camera, SurveyType

admin.site.Register(Camera)
admin.site.Register(SurveyType)
