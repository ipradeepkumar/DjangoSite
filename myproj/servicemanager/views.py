import socket 
import os
import io
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
import time
from servicemanager.api.serializers import TaskSerializer
from .forms import TaskForm
from .models import Idea, Platform, Station, Task, TaskIteration, TaskStatus, Tool, EmonCounter, EmonEvent
from datetime import datetime
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .customdecorator import ldap_auth
from django_python3_ldap import ldap
from django.contrib.auth import logout, login



# LDAP_URI = 'ldap://ldap.forumsys.com:389'
# LDAP_DN = 'dc=example,dc=com'
# LDAP_USERNAME = 'einstein'
# LDAP_PASSWORD = 'password'
# USER_NAME = 'einstein'
# USER_IN_GROUP = 'CN=Scientist,DC=example,DC=com'


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
        return HttpResponseRedirect("/")
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
        
        emonCounterData = EmonCounter.objects.filter(EmonCounterID__in = taskFormObj.cleaned_data['EmonCounters']).values_list('Name', flat=True)
        emonEventData = EmonEvent.objects.filter(EmonEventID__in = taskFormObj.cleaned_data['EmonEvents']).values_list('Name', flat=True)
        task = Task(
            Idea = taskFormObj.cleaned_data['Idea'],
            Station= taskFormObj.cleaned_data['Stations'],
            IsDebugMode = taskFormObj.cleaned_data['DebugMode'],
            PlatformCounter = list(emonCounterData),
            PlatformEvent = list(emonEventData),
            TotalIterations = taskFormObj.cleaned_data['TotalIterations'],
            RegressionName = taskFormObj.cleaned_data['RegressionName'],
            Tool = taskFormObj.cleaned_data['ToolName'],
            Platform = taskFormObj.cleaned_data['Platform'],
            IsEmon = taskFormObj.cleaned_data['IsEmon'],
            IsUploadResults = taskFormObj.cleaned_data['IsUploadResult'],
            Splitter = "Splitter",
            MinImpurityDecrease = "0.5",
            MaxFeatures = "0.9",
            CreatedBy = request.user.username,
            CreatedDate = datetime.now(),
            Status = "PENDING"
            )
        task.save()
        taskJson = serializers.serialize('json', [task])
        return HttpResponseRedirect("jobhistory")
   

    return render(request, "servicemanager/newtask.html", {
        "taskForm": taskFormObj
    })

def find(task: Task, condition):
    if (task.Status == condition):
        return task
        
@ldap_auth
def jobhistory(request):
    taskList = Task.objects.all().filter(CreatedBy = request.user.username).order_by("-id")
    taskIterations = TaskIteration.objects.all().order_by("-id")
    return render(request, "servicemanager/jobhistory.html", {
        "tasks": taskList, "colNames" : Task._meta.fields, "iterations" : taskIterations
    })

def jobhistory_detail(request, id):
    pass

def customlogout(request):
    logout(request)
    return render(request, "servicemanager/logout.html")

def StartProcess(request, GUID):
    instance = Task.objects.get_queryset().filter(GUID=GUID).first()
    ProcessTask(instance=instance)
    pass
    
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

def ProcessTask(instance): 
    isValid = False
    data = {
        "CurrentIteration": 0,
        "Status": 'IN-PROGRESS',
         "TestResults": '',
         "AxonLog": '',
         "IterationResult": '',
         "AzureLink": ""
    }
    serializer = TaskSerializer(instance=instance, data=data)
    if serializer.is_valid():
            serializer.save()
    TaskIteration.objects.filter(GUID=instance.GUID).delete()

    for i in range(instance.TotalIterations):
            data = {
                "CurrentIteration": str(i + 1),
                "Status": 'IN-PROGRESS',
                "TestResults": '{Passed: 3,Failed: 2}',
                "AxonLog": 'Logged data',
                "IterationResult": 'Results',
                "AzureLink": "http://www.google.com"
            }
            serializer = TaskSerializer(instance=instance, data=data)
            if serializer.is_valid():
                isValid = True
                serializer.save()

                taskIteration = TaskIteration()
                jsonData = { 'key1': (i + 1), 'key2': 'value2', 'key3': 'value3', 'key4': 'value4' }
                taskIteration.TaskID = instance.id
                taskIteration.GUID = instance.GUID
                taskIteration.JSONData = jsonData
                taskIteration.CreatedDate = datetime.now()
                taskIteration.Iteration = i + 1
                taskIteration.save()
                
                time.sleep(5)
    if (i == instance.TotalIterations - 1):
        compData = {
            "Status": 'COMPLETED'
        }
        compSerializer = TaskSerializer(instance=instance, data=compData)
        if compSerializer.is_valid():
            compSerializer.save()
    return isValid