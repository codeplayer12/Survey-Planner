from django.db import models

# Camera model.
class Camera(models.Model):
    camera_type = models.CharField(max_length=200)
    sensorw = models.FloatField()          
    sensorh = models.FloatField()
    pixelw  = models.IntegerField()
    pixelh = models.IntegerField()
    mpixel = models.FloatField()
    lensFocal = models.FloatField() 
    imageSize = models.FloatField() 
    comments = models.CharField(max_length=200,blank=True)
    
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
    flightTime =models.FloatField()
    pricing = models.IntegerField()
    comments = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.name

class BudgetItem(models.Model):
    name = models.CharField(max_length=50)
    unit = models.FloatField()
    unitCost = models.IntegerField()
    def __str__(self):
        return self.name