from pickle import FALSE
from platform import platform
from django.db import models


# Create your models here.
class Station(models.Model):
    StationID = models.IntegerField()
    Name = models.CharField(max_length=250)
    Desc = models.CharField(max_length=500)

class Tool(models.Model):
    ToolID = models.IntegerField(primary_key=True, unique=False)
    Name = models.CharField(max_length=150)

class ToolEvent(models.Model):
    ToolEventID = models.IntegerField(primary_key=True, unique=False)
    Name = models.CharField(max_length=150)
    Tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, related_name="toolevents")

class ToolCounter(models.Model):
    ToolCounterID = models.IntegerField(primary_key=True, unique=False)
    Name = models.CharField(max_length=150)
    ToolEvent = models.ForeignKey(ToolEvent, on_delete=models.SET_NULL, null=True, related_name="toolcounterevents")

class Platform(models.Model):
    PlatformID = models.IntegerField()
    Name = models.CharField(max_length=150)

class EmonEvent(models.Model):
    EmonEventID = models.IntegerField()
    Name = models.CharField(max_length=150)
    Platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, related_name="emonevents")

class EmonCounter(models.Model):
    EmonCounterID = models.IntegerField()
    Name = models.CharField(max_length=150)
    EmonEvent = models.ForeignKey(EmonEvent, on_delete=models.SET_NULL, null=True, related_name="emoncounters")

class Idea(models.Model):
    IdeaID = models.IntegerField()
    Name = models.CharField(max_length=200)

class TaskStatus(models.Model):
    TaskStatusID = models.IntegerField()
    Name = models.CharField(max_length=50)

class Task(models.Model):
    TaskID: models.IntegerField()
    Station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    IsDebugMode = models.BooleanField(default=FALSE)
    RegressionName = models.CharField(max_length=250)
    Tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True)
    ToolEvent = models.ForeignKey(ToolEvent, on_delete=models.SET_NULL, null=True)
    ToolCounter = models.ForeignKey(ToolCounter, on_delete=models.SET_NULL, null=True)
    Platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True)
    IsEmon = models.BooleanField(default=False)
    PlatformEvent = models.ForeignKey(EmonEvent, on_delete=models.SET_NULL, null=True)
    PlatformCounter = models.ForeignKey(EmonCounter, on_delete=models.SET_NULL, null=True)
    Idea = models.ForeignKey(Idea, on_delete=models.SET_NULL, null=True)
    IsUploadResults = models.BooleanField(default=False)
    TotalIterations = models.IntegerField()
    Splitter = models.CharField(max_length=50)
    MinImpurityDecrease = models.CharField(max_length=50)
    MaxFeatures = models.CharField(max_length=50)
    CreatedBy = models.CharField(max_length=50)
    CreatedDate = models.DateField()
    ModifiedBy = models.CharField(max_length=50)
    ModifiedDate = models.DateField()
    ErrorCode = models.CharField(max_length=10)
    ErrorMessage = models.CharField(max_length=500)
    Status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True)




