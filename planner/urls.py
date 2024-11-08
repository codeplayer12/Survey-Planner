from django.contrib import admin
from django.urls import path

from . import views


admin.site.site_header = "Survery Planner Admin"
admin.site.site_title = "Survey Planner | Budget Calculator"
admin.site.index_title = "Survey Planner"

urlpatterns = [
    path('', views.index, name='index'),
    path('drone',views.get_drone_values,name="drone"),
    path('survey',views.get_survey_values,name="survey"),
    path('budget',views.budget_calc,name="budget"),
    path('budget_adjustment',views.budget_adjustment,name='budget_adjustment'),
    # path('home',views.home,name='home')
]