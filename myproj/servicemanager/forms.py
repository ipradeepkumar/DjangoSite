from django import forms

class TaskForm(forms.Form):
    TotalIterations = forms.IntegerField(required=False, label="Total Iterations", widget = forms.TextInput(attrs={"class":"form-control", "placeholder": "Please enter Iterations"}))
    RegressionName = forms.CharField(required=False, max_length=100, label="Regression Name", widget = forms.TextInput(attrs={"class":"form-control", "placeholder": "Please enter regression name"}))
    Idea = forms.CharField(required=False, max_length=150, label="Idea", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: follow_all |follow_max | follow_min"}))
    Splitter = forms.CharField(required=False, max_length=50, label="Splitter", widget = forms.TextInput(attrs={"class":"form-control","placeholder":"eg: random | best"}))
    MinImpurityDecrease = forms.CharField(required=False, max_length=50, label="Min Impurity decrease", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))
    MaxFeatures = forms.CharField(required=False, max_length=50, label="Max Features", widget = forms.TextInput(attrs={"class":"form-control", "placeholder":"eg: 0.1 <= your_value <= 1.0"}))