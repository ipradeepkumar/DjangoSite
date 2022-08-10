from django import forms
import os
import io
from rest_framework.parsers import JSONParser



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

class TaskForm(forms.Form):
    Stations = ChoiceFieldNoValidation(label="Station", widget=forms.Select(attrs={"class":"form-control", "id":"ddlStation"}))
    DebugMode = forms.BooleanField(label="Debug Mode", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkDebug", "autocomplete":"off"}))
    RegressionName = forms.CharField(required=False, max_length=100, label="Regression Name", widget = forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder": "Please enter regression name"}))
    TotalIterations = forms.IntegerField(required=False, label="Total Iterations", widget = forms.NumberInput(attrs={ "min":"0", "class":"form-control", "autocomplete":"off", "placeholder": "Please enter Iterations"}))
    ToolName = MultipleChoiceFieldNoValidation(label="Tool Name", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolName"}))
    #ToolEvents = forms.MultipleChoiceField(label="Tool Events", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolEvents"}))
    #ToolCounters = forms.MultipleChoiceField(label="Tool Counter", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolCounters"}))
    Platform = ChoiceFieldNoValidation(label="Platform", widget=forms.Select(attrs={"class":"form-control", "id":"ddlPlatform"}))
    IsEmon = forms.BooleanField(label="Emon Tool", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkEmon"}))
    EmonEvents = MultipleChoiceFieldNoValidation(label="Emon Events", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlEmonEvents"}))
    EmonCounters = MultipleChoiceFieldNoValidation(label="Emon Counter", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlEmonCounters"}))
    Idea = ChoiceFieldNoValidation(label="Idea", widget=forms.Select(attrs={"class":"form-control", "id":"ddlIdea"}))
    IsUploadResult = forms.BooleanField(label="Upload Result", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkUploadResult"}))
    
    #Splitter = forms.CharField(required=False, max_length=50, label="Splitter", widget = forms.TextInput(attrs={"class":"form-control","placeholder":"eg: random | best"}))
    #MinImpurityDecrease = forms.CharField(required=False, max_length=50, label="Min Impurity decrease", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
    #MaxFeatures = forms.CharField(required=False, max_length=50, label="Max Features", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
