import socket 
import os
import io
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
import time
from servicemanager.api.serializers import TaskSerializer
from .forms import TaskForm
from .models import Idea, Platform, Station, Task, TaskExecutionLog, TaskIteration, TaskStatus, Tool, EmonCounter, EmonEvent
from datetime import datetime
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .customdecorator import ldap_auth
from django_python3_ldap import ldap
from django.contrib.auth import logout, login, models 
from multiprocessing import Process
import requests


# LDAP_URI = 'ldap://ldap.forumsys.com:389'
# LDAP_DN = 'dc=example,dc=com'
# LDAP_USERNAME = 'einstein'
# LDAP_PASSWORD = 'password'
# USER_NAME = 'einstein'
# USER_IN_GROUP = 'CN=Scientist,DC=example,DC=com'

dictThreads = {}

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
        return HttpResponseRedirect("jobhistory", { "id": "123" })
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
            Station= taskFormObj.cleaned_data['Stations'].split('^')[1],
            IsDebugMode = taskFormObj.cleaned_data['DebugMode'],
            PlatformCounter = list(emonCounterData),
            PlatformEvent = list(emonEventData),
            TotalIterations = taskFormObj.cleaned_data['TotalIterations'],
            RegressionName = taskFormObj.cleaned_data['RegressionName'],
            Tool = taskFormObj.cleaned_data['ToolName'],
            Platform = taskFormObj.cleaned_data['Stations'].split('^')[0],
            IsEmon = taskFormObj.cleaned_data['IsEmon'],
            IsUploadResults = taskFormObj.cleaned_data['IsUploadResult'],
            Splitter = taskFormObj.cleaned_data['Splitter'],
            MinImpurityDecrease = taskFormObj.cleaned_data['MinImpurityDecrease'],
            MaxFeatures = taskFormObj.cleaned_data['MaxFeatures'],
            CreatedBy = request.user.username,
            CreatedDate = datetime.utcnow(),
            Status = "PENDING"
            )
        task.save()

        station = Station.objects.get(Name=taskFormObj.cleaned_data['Stations'].split('^')[1])
        station.IsActive = False
        station.save();

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
    taskList = Task.objects.all()
    taskIterations = TaskIteration.objects.all().order_by("-id")
    usrs = models.User.objects.all().values('username')
    return render(request, "servicemanager/jobhistory.html", {
        "tasks": taskList, "colNames" : Task._meta.fields, "iterations" : taskIterations, "Users": usrs
    })

def jobhistory_detail(request, id):
    pass

def customlogout(request):
    logout(request)
    return render(request, "servicemanager/logout.html")

def StartProcess(request, GUID, userExecution, eowynExecution):
    instance = Task.objects.get_queryset().filter(GUID=GUID).first()
    try:
        #update task with flags received from front-end
        #userExecution and eowyn execution is set to true when user triggers the process
        #userExecution is set to false when user stops the process
        #eowynExecution is false when python updates to false when user stops the process
        #Task status save
        instance.IsUserExecution = userExecution
        instance.IsEowynExecution = eowynExecution
        

        if (userExecution):
            SaveTaskExecutionLog(request, instance, 'START')
            instance.Status = 'STARTING'
            instance.save()
        elif(userExecution == False):
            SaveTaskExecutionLog(request, instance, 'STOPPED')
            instance.Status = 'STOPPING'
            instance.save()

        if (userExecution):
            req = requests.post("http://127.0.0.1:8000/api/posttask/", data = { "GUID" : instance.GUID } )
        
        response = {
            'status': '200', 'responseText': 'success'
        }
        return JsonResponse(response)
    except Exception as e:
        response = {
            'status': '500', 'responseText': 'error'
        }
        return JsonResponse(response)
    
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
    ClearPreviousRunData(instance)
    for i in range(instance.TotalIterations):
        if (GetExecutionStatus(instance)):
            data = {
                "CurrentIteration": str(i + 1),
                "Status": 'IN-PROGRESS',
                "TestResults": '{Passed: ' + str(i + 1) +' ,Failed: 0 }',
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
                
                time.sleep(10)
            if (i == instance.TotalIterations - 1):
                compData = {
                    "Status": 'COMPLETED'
                }
                compSerializer = TaskSerializer(instance=instance, data=compData)
                if compSerializer.is_valid():
                    compSerializer.save()
                return isValid
        else:
            process = dictThreads[instance.GUID]
            process.close()
            process.kill()
            break
    return False
        

def SaveTaskExecutionLog(req, instance, status):
        executionLog = TaskExecutionLog(
        TaskID = instance.TaskID,
        GUID = instance.GUID,
        StatusDate = datetime.utcnow(),
        Status = status,
        CreatedBy = req.user.username,
        CreatedDate = datetime.utcnow()) 
        executionLog.save()
    
def ClearPreviousRunData(instance):
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

def GetExecutionStatus(taskInstance):
    instance = Task.objects.get_queryset().filter(GUID=taskInstance.GUID).first()
    if (instance.IsUserExecution == False):
        instance.IsEowynExecution = False
        instance.Status = 'STOPPED'
        instance.save()
    return instance.IsUserExecution


def GetStationList():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "api", "data", "station.json")
    with open(filePath, 'r') as stationfile:
        stream = io.BytesIO(str.encode(stationfile.read()))
        stationData = JSONParser().parse(stream=stream)
        return stationData

def GetToolList():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "api", "data", "tool.json")
    with open(filePath, 'r') as toolfile:
        stream = io.BytesIO(str.encode(toolfile.read()))
        toolData = JSONParser().parse(stream=stream)
        return toolData