from django.db import models

# Camera model.
class Camera(models.Model):
    camera_type = models.CharField(max_length=200)
    sensorw = models.DecimalField()           
    sensorh = models.DecimalField()
    pixelw  = models.IntegerField()
    pixelh = models.IntegerField()
    mpixel = models.DecimalField() 
    lensFocal = models.DecimalField() 
    imageSize = models.DecimalField() 
    comments = models.CharField(max_length=200)
    
    def __str__(self):
        return self.camera_type

    
class SurveyType(models.Model):
    name = models.CharField(max_length=50)
    forward = models.IntegerField()
    lateral = models.IntegerField()

    def __str__(self):
        return self.name