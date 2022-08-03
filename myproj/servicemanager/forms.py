from django import forms

class TaskForm(forms.Form):
    Stations = forms.ChoiceField(label="Station", widget=forms.Select(attrs={"class":"form-control", "id":"ddlStation"}))
    DebugMode = forms.BooleanField(label="Debug Mode", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkDebug"}))
    RegressionName = forms.CharField(required=False, max_length=100, label="Regression Name", widget = forms.TextInput(attrs={"class":"form-control", "placeholder": "Please enter regression name"}))
    TotalIterations = forms.IntegerField(required=False, label="Total Iterations", widget = forms.TextInput(attrs={"class":"form-control", "placeholder": "Please enter Iterations"}))
    ToolName = forms.MultipleChoiceField(label="Tool Name", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolName"}))
    #ToolEvents = forms.MultipleChoiceField(label="Tool Events", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolEvents"}))
    #ToolCounters = forms.MultipleChoiceField(label="Tool Counter", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlToolCounters"}))
    Platform = forms.ChoiceField(label="Platform", widget=forms.Select(attrs={"class":"form-control", "id":"ddlPlatform"}))
    IsEmon = forms.BooleanField(label="Emon Tool", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkEmon"}))
    EmonEvents = forms.MultipleChoiceField(label="Emon Events", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlEmonEvents"}))
    EmonCounters = forms.MultipleChoiceField(label="Emon Counter", widget=forms.SelectMultiple(attrs={"class":"form-control", "id":"ddlEmonCounters"}))
    Idea = forms.ChoiceField(label="Idea", widget=forms.Select(attrs={"class":"form-control", "id":"ddlIdea"}))
    IsUploadResult = forms.BooleanField(label="Upload Result", widget=forms.CheckboxInput(attrs={"class":"form-control", "id":"chkUploadResult"}))
    
    #Splitter = forms.CharField(required=False, max_length=50, label="Splitter", widget = forms.TextInput(attrs={"class":"form-control","placeholder":"eg: random | best"}))
    #MinImpurityDecrease = forms.CharField(required=False, max_length=50, label="Min Impurity decrease", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
    #MaxFeatures = forms.CharField(required=False, max_length=50, label="Max Features", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))