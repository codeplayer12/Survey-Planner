from django.db import models

# Camera model.
class Camera(models.Model):
    camera_type = models.CharField(max_length=200)
    sensorw = models.FloatField()          
    sensorh = models.FloatField()
    pixelw = models.IntegerField()
    pixelh = models.IntegerField()
    mpixel = models.FloatField()
    lensFocal = models.FloatField() 
    imageSize = models.FloatField() 
    comments = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.camera_type

    
class SurveyType(models.Model):
    name = models.CharField(max_length=50)
    forward = models.IntegerField()
    lateral = models.IntegerField()

    def __str__(self):
        return self.name

class Drone(models.Model):
    name = models.CharField(max_length=30)
    cruiseSpeed = models.FloatField()
    flightTime = models.FloatField()
    pricing = models.IntegerField()
    comments = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=30)  
    def __str__(self):
        return self.name  

class BudgetItem(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class PlannerValue(models.Model):
    number_of_flights = models.IntegerField()
    orthophoto_resolution = models.FloatField()
    dsm_resolution = models.FloatField()
    total_number_of_images_captured = models.IntegerField()
    number_of_gigapixels = models.FloatField()
    total_size_of_digital_files = models.FloatField()
    battery_capacity = models.IntegerField()
    flight_height = models.FloatField()
    take_off_area_distance = models.IntegerField()
    area_size = models.IntegerField()
    distance_travelled_per_flight = models.FloatField()
    duration_of_mission = models.IntegerField()
    camera_id = models.IntegerField()
    drone_id = models.IntegerField()
    survey_type_id = models.IntegerField()
        
class BudgetEstimate(models.Model):
    cost = models.FloatField()

    def __str__(self):
        return self.cost

class DepartmentCost(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_Cost = models.FloatField()

    def __str__(self):
        return self.department.name

class BudgetItemCost(models.Model):
    budget_item = models.ForeignKey(BudgetItem, on_delete=models.CASCADE)
    days = models.FloatField(blank = True, null = True)
    unitCost = models.FloatField()
    units = models.FloatField(blank =True, null =True)
    totalCost = models.FloatField()

    def __str__(self):
        return self.budget_item.name

class Default(models.Model):
    drone = models.IntegerField()
    camera = models.IntegerField()
    surveyType = models.IntegerField()
    batteryCapacity = models.IntegerField()
    areaSize  = models.IntegerField()
    selectedMeasure = models.CharField(max_length=255)
    distance_travelled_per_flight = models.FloatField() 
    take_of_area_distance  = models.FloatField()
