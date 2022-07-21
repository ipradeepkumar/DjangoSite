from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import TaskForm
from .models import Task

# Create your views here.
def index(request):
    return render(request, "servicemanager/index.html")

def newtask(request):
    if request.method == "GET":
        taskFormObj = TaskForm()

    if request.method == "POST":
        taskFormObj = TaskForm(request.POST)

    if taskFormObj.is_valid():
        print(taskFormObj.cleaned_data)
        task = Task(
            Idea = taskFormObj.cleaned_data['Idea'],
            Station="Test Station",
            Counter = "1,3",
            Events = "3,4",
            TotalIterations = taskFormObj.cleaned_data['TotalIterations'],
            RegressionName = taskFormObj.cleaned_data['RegressionName'],
            Splitter = taskFormObj.cleaned_data['Splitter'],
            MinImpurityDecrease = taskFormObj.cleaned_data['MinImpurityDecrease'],
            MaxFeatures = taskFormObj.cleaned_data['MaxFeatures'],
            )
        task.save()
       
        return HttpResponseRedirect("jobhistory")
    else:    
        taskFormObj = TaskForm()

    return render(request, "servicemanager/newtask.html", {
        "taskForm": taskFormObj
    })

def jobhistory(request):
    return render(request, "servicemanager/jobhistory.html")


def jobhistory_detail(request, jobid):
    pass
