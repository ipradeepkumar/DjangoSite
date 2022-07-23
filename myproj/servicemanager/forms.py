from django import forms

class TaskForm(forms.Form):
    eventOptions = (("","ALL"), ("1","INST_RETIRED_ANY"), ("2","CPU_CLK_UNHALTED_THREAD"), ("3","CPU_CLK_UNHALTED_REF_TSC"), ("4","TOPDOWN_SLOTS") )
    stationOptions = (("",""), ("0","ICX-D2 SW2 sockets 40 cores | JF04WVAW0722"))
    counterOptions = (("","ALL"), ("1","POC0TO"), ("2","POC1TO"), ("3","POC2TO"), ("4","POC3TO"))
    Stations = forms.ChoiceField(label="Station", widget=forms.Select(attrs={"class":"form-control"}), choices=stationOptions)
    Events = forms.MultipleChoiceField(label="Events", widget=forms.SelectMultiple(attrs={"class":"form-control"}), choices=eventOptions)
    Counters = forms.MultipleChoiceField(label="Counter", widget=forms.SelectMultiple(attrs={"class":"form-control"}), choices=counterOptions)
    TotalIterations = forms.IntegerField(required=False, label="Total Iterations", widget = forms.TextInput(attrs={"class":"form-control", "placeholder": "Please enter Iterations"}))
    RegressionName = forms.CharField(required=False, max_length=100, label="Regression Name", widget = forms.TextInput(attrs={"class":"form-control", "placeholder": "Please enter regression name"}))
    Idea = forms.CharField(required=False, max_length=150, label="Idea", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: follow_all |follow_max | follow_min"}))
    Splitter = forms.CharField(required=False, max_length=50, label="Splitter", widget = forms.TextInput(attrs={"class":"form-control","placeholder":"eg: random | best"}))
    MinImpurityDecrease = forms.CharField(required=False, max_length=50, label="Min Impurity decrease", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
    MaxFeatures = forms.CharField(required=False, max_length=50, label="Max Features", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))