from django.contrib import admin

# Register your models here.
from .models import Camera, SurveyType, Drone, BudgetItem, Department, BudgetEstimate, BudgetItemCost, DepartmentCost, Default,PlannerValue, AreaSizeAndUnit, Currency

admin.site.register(Camera)
admin.site.register(SurveyType)
admin.site.register(Drone)
admin.site.register(BudgetItem)
admin.site.register(Department)
admin.site.register(BudgetEstimate)
admin.site.register(BudgetItemCost)
admin.site.register(DepartmentCost)
admin.site.register(PlannerValue)
admin.site.register(AreaSizeAndUnit)
admin.site.register(Default)
admin.site.register(Currency)
