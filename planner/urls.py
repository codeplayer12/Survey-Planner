from django.contrib import admin
from django.urls import path

from . import views


admin.site.site_header = "Survery Planner Admin"
admin.site.site_title = "Survey Planner | Budget Calculator"
admin.site.index_title = "Survey Planner"

urlpatterns = [
    path('', views.index, name='index'),
]