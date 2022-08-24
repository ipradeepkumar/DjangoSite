import socket 
import os
import io
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .forms import TaskForm
from .models import Idea, Platform, Station, Task, TaskStatus, Tool
from datetime import datetime
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .customdecorator import ldap_auth
from django_python3_ldap.utils import format_search_filters
from django_python3_ldap import ldap
from django.contrib.auth import logout, login

LDAP_URI = 'ldap://ldap.forumsys.com:389'
LDAP_DN = 'dc=example,dc=com'
LDAP_USERNAME = 'einstein'
LDAP_PASSWORD = 'password'
USER_NAME = 'einstein'
USER_IN_GROUP = 'CN=Scientist,DC=example,DC=com'


@ldap_auth
def test_ldap(request):
    print('actual method')
    return HttpResponse("Welcome to private page")


def doLogin(request):
    if request.method == "GET":
        return render(request, "servicemanager/login.html")
    
    if request.method == "POST":
       username = request.POST.get('txtUsername')
       password = request.POST.get('txtPassword')
       user = ldap.authenticate(username=username, password=password)
       if (user is not None):
        login(request, user)
        return render(request, "servicemanager/index.html",{ "error": "" })
       else:
        return render(request, "servicemanager/login.html",{ "error": "Invalid credentials" })

@ldap_auth
def index(request):
    return render(request, "servicemanager/index.html")

@ldap_auth
def newtask(request):
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)  
    if request.method == "GET":
        taskFormObj = TaskForm()

    if request.method == "POST":
        taskFormObj = TaskForm(request.POST)

    if taskFormObj.is_valid():
        print(taskFormObj.cleaned_data)
        task = Task(
            Idea = taskFormObj.cleaned_data['Idea'],
            Station= taskFormObj.cleaned_data['Stations'],
            IsDebugMode = taskFormObj.cleaned_data['DebugMode'],
            PlatformCounter = taskFormObj.cleaned_data['EmonCounters'],
            PlatformEvent = taskFormObj.cleaned_data['EmonEvents'],
            TotalIterations = taskFormObj.cleaned_data['TotalIterations'],
            RegressionName = taskFormObj.cleaned_data['RegressionName'],
            Tool = taskFormObj.cleaned_data['ToolName'],
            Platform = taskFormObj.cleaned_data['Platform'],
            IsEmon = taskFormObj.cleaned_data['IsEmon'],
            IsUploadResults = taskFormObj.cleaned_data['IsUploadResult'],
            Splitter = "Splitter",
            MinImpurityDecrease = "0.5",
            MaxFeatures = "0.9",
            CreatedBy = IPAddr,
            CreatedDate = datetime.now(),
            Status = "PENDING"
            )
        task.save()
        taskJson = serializers.serialize('json', [task])
        print(taskJson)
        return HttpResponseRedirect("jobhistory")
   

    return render(request, "servicemanager/newtask.html", {
        "taskForm": taskFormObj
    })

def find(task: Task, condition):
    if (task.Status == condition):
        return task
@ldap_auth
def jobhistory(request):
    if (request.META.get("HTTP_REFERER")):
        inprogressList = Task.objects.filter(Status = "IN-PROGRESS")
        if (inprogressList.count() > 0):
            inprogress = inprogressList[0]
            inprogress.Status = 'COMPLETE'
            inprogress.save()

        if (request.META.get("HTTP_REFERER").__contains__("jobhistory")):
            pendingList = Task.objects.filter(Status = "PENDING")
            if (pendingList.count() > 0):
                pending = pendingList[0]
                pending.Status = 'IN-PROGRESS'
                pending.save()

            

    taskList = Task.objects.all()
    return render(request, "servicemanager/jobhistory.html", {
        "tasks": taskList, "colNames" : Task._meta.fields
    })

def jobhistory_detail(request, id):
    pass

def customlogout(request):
    logout(request)
    return render(request, "servicemanager/logout.html")

class TaskDetailView(DetailView):
    model = Task
    template_name = "servicemanager/jobhistorydetail.html"

def getStationInstance(stationID):
     dirPath = os.path.dirname(os.path.realpath(__file__))
     filePath = os.path.join(dirPath, "api", "data", "station.json")
     with open(filePath, 'r') as stationfile:
        stream = io.BytesIO(str.encode(stationfile.read()))
        stationData = JSONParser().parse(stream=stream)
        stationObj = Station()
        for station in stationData:
            if (station["StationID"] == stationID):
                stationObj.StationID = station["StationID"]
                stationObj.Name = station["Name"]
        return stationObj

def getToolInstance(toolID):
     dirPath = os.path.dirname(os.path.realpath(__file__))
     filePath = os.path.join(dirPath, "api", "data", "tool.json")
     with open(filePath, 'r') as toolfile:
        stream = io.BytesIO(str.encode(toolfile.read()))
        toolData = JSONParser().parse(stream=stream)
        toolObj = Tool()
        for tool in toolData:
            if (tool["ToolID"] == toolID):
                toolObj.ToolID = tool["ToolID"]
                toolObj.Name = tool["Name"]
        return toolObj

def getPlatformInstance(platformID):
     dirPath = os.path.dirname(os.path.realpath(__file__))
     filePath = os.path.join(dirPath, "api", "data", "platform.json")
     with open(filePath, 'r') as platformfile:
        stream = io.BytesIO(str.encode(platformfile.read()))
        platformData = JSONParser().parse(stream=stream)
        platformObj = Platform()
        for platform in platformData:
            if (platform["PlatformID"] == platformID):
                platformObj.PlatformID = platform["PlatformID"]
                platformObj.Name = platform["Name"]
        return platformObj

def getIdeaInstance(ideaID):
     dirPath = os.path.dirname(os.path.realpath(__file__))
     filePath = os.path.join(dirPath, "api", "data", "idea.json")
     with open(filePath, 'r') as ideafile:
        stream = io.BytesIO(str.encode(ideafile.read()))
        ideaData = JSONParser().parse(stream=stream)
        ideaObj = Idea()
        for idea in ideaData:
            if (idea["IdeaID"] == ideaID):
                ideaObj.IdeaID = idea["IdeaID"]
                ideaObj.Name = idea["Name"]
        return ideaObj

def getTaskStatusInstance():
    taskStatus = TaskStatus()
    taskStatus.TaskStatusID = 1
    taskStatus.Name = "Pending"
    return taskStatus



                    

        