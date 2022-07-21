
from django.db import models


# Create your models here.
 
class Task(models.Model):
    Station = models.CharField(max_length=50)
    Counter = models.CharField(max_length=25)
    Events = models.CharField(max_length=25)
    TotalIterations = models.IntegerField()
    RegressionName = models.CharField(max_length=100)
    Idea = models.CharField(max_length=150)
    Splitter = models.CharField(max_length=50)
    MinImpurityDecrease = models.CharField(max_length=50)
    MaxFeatures = models.CharField(max_length=50)