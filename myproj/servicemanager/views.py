from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
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
            Station= taskFormObj.cleaned_data['Stations'],
            Counter = taskFormObj.cleaned_data['Counters'],
            Events = taskFormObj.cleaned_data['Events'],
            TotalIterations = taskFormObj.cleaned_data['TotalIterations'],
            RegressionName = taskFormObj.cleaned_data['RegressionName'],
            Splitter = taskFormObj.cleaned_data['Splitter'],
            MinImpurityDecrease = taskFormObj.cleaned_data['MinImpurityDecrease'],
            MaxFeatures = taskFormObj.cleaned_data['MaxFeatures'],
            )
        task.save()
       
        return HttpResponseRedirect("jobhistory")
   

    return render(request, "servicemanager/newtask.html", {
        "taskForm": taskFormObj
    })

def jobhistory(request):
    taskList = Task.objects.all()
    return render(request, "servicemanager/jobhistory.html", {
        "tasks": taskList, "colNames" : Task._meta.fields
    })

def jobhistory_detail(request, id):
    task = Task.objects.get(pk = id)
    return render(request, "servicemanager/jobhistorydetail.html", {
        "task": task
    })


class TaskDetailView(DetailView):
    model = Task
    template_name = "servicemanager/jobhistorydetail.html"
     


  
