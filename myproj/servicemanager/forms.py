from pickle import FALSE
from django import forms
import os
import io
from rest_framework.parsers import JSONParser
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from servicemanager.models import TaskIteration



def getTools():
     dirPath = os.path.dirname(os.path.realpath(__file__))
     filePath = os.path.join(dirPath, "api", "data", "tool.json")
     with open(filePath, 'r') as toolfile:
        stream = io.BytesIO(str.encode(toolfile.read()))
        toolData = JSONParser().parse(stream=stream)
        tools = []
        for tool in toolData:
            tools.append((tool["ToolID"], tool["Name"]))
        return tools

class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
       pass
    
class TaskEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
class TaskForm(forms.Form):
    Stations = ChoiceFieldNoValidation(label="Station", widget=forms.Select(attrs={"class":"form-control", "id":"ddlStation"}, ))
    DebugMode = forms.BooleanField(label="Debug Mode", required=False, widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkDebug", "autocomplete":"off"}))
    RegressionName = forms.CharField(required=False, max_length=100, label="Regression Name", widget = forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder": "Please enter regression name"}))
    TotalIterations = forms.IntegerField(required=False, label="Total Iterations", widget = forms.NumberInput(attrs={ "min":"0", "class":"form-control", "autocomplete":"off", "placeholder": "Please enter Iterations"}))
    ToolName = ChoiceFieldNoValidation(label="Tool Name", widget=forms.Select(attrs={"class":"form-control", "id":"ddlToolName"}))
    #ToolEvents = forms.MultipleChoiceField(label="Tool Events", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolEvents"}))
    #ToolCounters = forms.MultipleChoiceField(label="Tool Counter", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolCounters"}))
    Platform = ChoiceFieldNoValidation(label="Platform", widget=forms.Select(attrs={"class":"form-control", "id":"ddlPlatform"}))
    IsEmon = forms.BooleanField(required=False,label="Emon Tool", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkEmon"}))
    EmonEvents = MultipleChoiceFieldNoValidation(required=False,label="Emon Events", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlEmonEvents"}))
    EmonCounters = MultipleChoiceFieldNoValidation(required=False,label="Emon Counter", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlEmonCounters"}))
    Idea = ChoiceFieldNoValidation(label="Idea", widget=forms.Select(attrs={"class":"form-control", "id":"ddlIdea"}))
    IsUploadResult = forms.BooleanField(required=False, label="Upload Result", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkUploadResult"}))
    Splitter = forms.CharField(required=False, max_length=50, label="Splitter", widget = forms.TextInput(attrs={"class":"form-control","placeholder":"eg: random | best"}))
    MinImpurityDecrease = forms.CharField(required=False, max_length=50, label="Min Impurity decrease", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
    MaxFeatures = forms.CharField(required=False, max_length=50, label="Max Features", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
    ToolJson = forms.CharField(required=False, widget = forms.Textarea(attrs={"class":"form-control"}))

class TaskListForm(forms.Form):
    TaskID = forms.IntegerField(required=False)
    Station = forms.CharField(max_length=250, required=False)
    IsDebugMode = forms.BooleanField()
    RegressionName = forms.CharField(max_length=250)
    Tool = forms.CharField(max_length=250, required=False)
    ToolEvent = forms.CharField(max_length=500, required=False)
    ToolCounter = forms.CharField(max_length=500, required=False)
    Platform = forms.CharField(max_length=500, required=False)
    IsEmon = forms.BooleanField(required=False)
    PlatformEvent = forms.Textarea()
    PlatformCounter = forms.Textarea()
    Idea = forms.CharField(max_length=500, required=False)
    IsUploadResults = forms.BooleanField()
    TotalIterations = forms.IntegerField()
    Splitter = forms.CharField(max_length=50)
    MinImpurityDecrease = forms.CharField(max_length=50)
    MaxFeatures = forms.CharField(max_length=50)
    CreatedBy = forms.CharField(max_length=50)
    CreatedDate = forms.DateTimeField()
    ModifiedBy = forms.CharField(max_length=50, required=False)
    ModifiedDate = forms.DateTimeField(required=False)
    ErrorCode = forms.CharField(max_length=10, required=False)
    ErrorMessage = forms.CharField(max_length=500, required=False)
    Status = forms.CharField(max_length=50, required=False)
    GUID = forms.UUIDField()
    CurrentIteration = forms.IntegerField()
    IterationResult = forms.CharField(max_length= 500, required=False)
    TestResults = forms.CharField(max_length=500, required=False)
    AxonLog = forms.CharField(max_length=250, required=False)
    AzureLink = forms.CharField(max_length=250, required=False)
    IsUserExecution = forms.BooleanField(required=False)
    IsEowynExecution = forms.BooleanField(required=False)
    ToolJson = forms.Textarea()
    TaskIterations = forms.ModelMultipleChoiceField(queryset=TaskIteration.objects.all())
