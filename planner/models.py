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