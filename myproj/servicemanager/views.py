import socket 
import os
import io
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
import time
from servicemanager.api.serializers import TaskSerializer
from .forms import TaskEncoder, TaskForm, TaskListForm
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
from django.views.decorators.csrf import csrf_exempt
import json
from array import array

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
    emonEventData = []
    emonCounterData = []
  
    if request.method == "GET":
        taskFormObj = TaskForm()
       

    if request.method == "POST":
        taskFormObj = TaskForm(request.POST)
        station = Station.objects.get(Name=taskFormObj['Stations'].data.split('^')[1])

        if (station.IsActive == False):
            return render(request, "servicemanager/newtask.html", {
            "taskForm": taskFormObj, "message": "Station is already in use."
        })
        else:
            if taskFormObj.is_valid():
                if (taskFormObj.cleaned_data['IsEmon'] == True):
                    emonCounterData =  [ emoncounter.Name for emoncounter in EmonCounter.objects.filter(EmonCounterID__in = taskFormObj.cleaned_data['EmonCounters'])] #.values_list('Name', flat=True)
                    emonEventData = [ emonevent.Name for emonevent in EmonEvent.objects.filter(EmonEventID__in = taskFormObj.cleaned_data['EmonEvents'])] #.values_list('Name', flat=True)
              
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
                    Status = "PENDING",
                    ToolJson = taskFormObj.cleaned_data['ToolJson'].replace("\r\n\t","").replace("\r\n",""),
                    )
                task.save()
                station.IsActive = False
                station.save()

                toolObj = Tool.objects.filter(Name = task.Tool, StationName = task.Station).first()
                toolObj.JsonFile = task.ToolJson
                toolObj.save()
                # taskJson = serializers.serialize('json', [task])
                return HttpResponseRedirect("jobhistorynewpageload")
   
# ALTER TABLE public.servicemanager_task 
# DROP COLUMN "PlatformEvent";    

# ALTER TABLE public.servicemanager_task  
# DROP COLUMN "PlatformCounter"; 

# ALTER TABLE public.servicemanager_task 
# ADD COLUMN "PlatformEvent" Text;

# ALTER TABLE public.servicemanager_task 
# ADD COLUMN "PlatformCounter" Text;

    return render(request, "servicemanager/newtask.html", {
        "taskForm": taskFormObj
    })

def find(task: Task, condition):
    if (task.Status == condition):
        return task
        
@ldap_auth
def jobhistory(request):
    taskList = Task.objects.all()
    #taskIterations = TaskIteration.objects.all().sort(key=lambda x: x["id"], reverse=True)
    taskIterations = TaskIteration.objects.all().order_by("-id")
    usrs = models.User.objects.all().values('username')
    return render(request, "servicemanager/jobhistory.html", {
        "tasks": taskList, "colNames" : Task._meta.fields, "iterations" : taskIterations, "Users": usrs
    })

@ldap_auth
def jobhistorynewpageload(request):
    usrs = models.User.objects.all().values('username')
    return render(request, "servicemanager/jobhistorynew.html", { "Users": usrs })

@ldap_auth
def jobhistorynew(request):
    taskList = Task.objects.filter(CreatedBy = request.user.username)
    taskListForm = []
    for i in range(len(taskList)):
        taskForm = {
        'TaskID': taskList[i].id if taskList[i].id is not None else '',
        'Station': taskList[i].Station,
        'IsDebugMode': taskList[i].IsDebugMode,
        'RegressionName': taskList[i].RegressionName,
        'Tool': taskList[i].Tool,
        'ToolEvent': taskList[i].ToolEvent if taskList[i].ToolEvent is not None else '',
        'ToolCounter': taskList[i].ToolCounter if taskList[i].ToolCounter is not None else '',
        'Platform': taskList[i].Platform,
        'IsEmon': taskList[i].IsEmon,
        'PlatformEvent': taskList[i].PlatformEvent,
        'PlatformCounter': taskList[i].PlatformCounter,
        'Idea': taskList[i].Idea,
        'IsUploadResults': taskList[i].IsUploadResults,
        'TotalIterations': taskList[i].TotalIterations,
        'Splitter': taskList[i].Splitter,
        'MinImpurityDecrease': taskList[i].MinImpurityDecrease,
        'MaxFeatures': taskList[i].MaxFeatures,
        'CreatedBy': taskList[i].CreatedBy,
        'CreatedDate': taskList[i].CreatedDate,
        'ModifiedBy': taskList[i].ModifiedBy if taskList[i].ModifiedBy is not None else '',
        'ModifiedDate': taskList[i].ModifiedDate if taskList[i].ModifiedDate is not None else '',
        'ErrorCode': taskList[i].ErrorCode if taskList[i].ErrorCode is not None else '',
        'ErrorMessage': taskList[i].ErrorMessage if taskList[i].ErrorMessage is not None else '',
        'Status': taskList[i].Status,
        'GUID': taskList[i].GUID,
        'CurrentIteration': taskList[i].CurrentIteration ,
        'IterationResult': taskList[i].IterationResult if taskList[i].IterationResult is not None else '',
        'TestResults': taskList[i].TestResults if taskList[i].TestResults is not None else '',
        'AxonLog': taskList[i].AxonLog if taskList[i].AxonLog is not None else '',
        'AzureLink': taskList[i].AzureLink if taskList[i].AzureLink is not None else '',
        'IsUserExecution': taskList[i].IsUserExecution if taskList[i].IsUserExecution is not None else '',
        'IsEowynExecution': taskList[i].IsEowynExecution if taskList[i].IsEowynExecution is not None else '',
        'ToolJson': taskList[i].ToolJson if taskList[i].ToolJson is not None else '',
        'TaskIterations': list(TaskIteration.objects.filter(GUID = str(taskList[i].GUID)).values())
        }
        taskListForm.append(taskForm)

    taskJson = json.dumps(taskListForm, cls= TaskEncoder)
    return JsonResponse({ "data": json.loads(taskJson) }, safe=False)

@ldap_auth
def jobhistorynewuser(request, user):
    if (user != 'all'):
     taskList = Task.objects.filter(CreatedBy = user)
    else:
     taskList = Task.objects.all()
    taskListForm = []
    for i in range(len(taskList)):
        taskForm = {
        'TaskID': taskList[i].id if taskList[i].id is not None else '',
        'Station': taskList[i].Station,
        'IsDebugMode': taskList[i].IsDebugMode,
        'RegressionName': taskList[i].RegressionName,
        'Tool': taskList[i].Tool,
        'ToolEvent': taskList[i].ToolEvent if taskList[i].ToolEvent is not None else '',
        'ToolCounter': taskList[i].ToolCounter if taskList[i].ToolCounter is not None else '',
        'Platform': taskList[i].Platform,
        'IsEmon': taskList[i].IsEmon,
        'PlatformEvent': taskList[i].PlatformEvent,
        'PlatformCounter': taskList[i].PlatformCounter,
        'Idea': taskList[i].Idea,
        'IsUploadResults': taskList[i].IsUploadResults,
        'TotalIterations': taskList[i].TotalIterations,
        'Splitter': taskList[i].Splitter,
        'MinImpurityDecrease': taskList[i].MinImpurityDecrease,
        'MaxFeatures': taskList[i].MaxFeatures,
        'CreatedBy': taskList[i].CreatedBy,
        'CreatedDate': taskList[i].CreatedDate,
        'ModifiedBy': taskList[i].ModifiedBy if taskList[i].ModifiedBy is not None else '',
        'ModifiedDate': taskList[i].ModifiedDate if taskList[i].ModifiedDate is not None else '',
        'ErrorCode': taskList[i].ErrorCode if taskList[i].ErrorCode is not None else '',
        'ErrorMessage': taskList[i].ErrorMessage if taskList[i].ErrorMessage is not None else '',
        'Status': taskList[i].Status,
        'GUID': taskList[i].GUID,
        'CurrentIteration': taskList[i].CurrentIteration ,
        'IterationResult': taskList[i].IterationResult if taskList[i].IterationResult is not None else '',
        'TestResults': taskList[i].TestResults if taskList[i].TestResults is not None else '',
        'AxonLog': taskList[i].AxonLog if taskList[i].AxonLog is not None else '',
        'AzureLink': taskList[i].AzureLink if taskList[i].AzureLink is not None else '',
        'IsUserExecution': taskList[i].IsUserExecution if taskList[i].IsUserExecution is not None else '',
        'IsEowynExecution': taskList[i].IsEowynExecution if taskList[i].IsEowynExecution is not None else '',
        'ToolJson': taskList[i].ToolJson if taskList[i].ToolJson is not None else '',
        'TaskIterations': list(TaskIteration.objects.filter(GUID = str(taskList[i].GUID)).values())
        }
        taskListForm.append(taskForm)

    taskJson = json.dumps(taskListForm, cls= TaskEncoder)
    return JsonResponse({ "data": json.loads(taskJson) }, safe=False)


# def jobhistory_detail(request, id):
#     pass

def customlogout(request):
    logout(request)
    return render(request, "servicemanager/logout.html")

def StartProcess(request, GUID, userExecution, eowynExecution): 
    instance = Task.objects.get_queryset().filter(GUID=GUID).first()
    #find any task with the same station is in-progress
    #if in-progress show an alert, else create a new task and start it
    #if we check for station active, we have tasks which are using the same station but never executed
    #in this case we can never start a task with same station which has been never executed
    #so checking for any task with same station and is in-progress
    if(True): 
        pass
    station = Station.objects.get(Name = instance.Station)
   
    # try:
    #     inProgressTask = Task.objects.get(Station=instance.Station, Status='IN-PROGRESS')
    # except Task.DoesNotExist:
    #     inProgressTask = None
    # if (inProgressTask != None):
    if (station.IsActive == False and (instance.Status == 'PENDING' or instance.Status == 'COMPLETED' or instance.Status == 'STOPPED' or instance.Status == 'ERROR')):
        response = {
                'status': '404', 'responseText': 'Job with this station is already active. Please try after sometime.'
            }
    else:
            if (instance.Status == 'PENDING' or instance.Status == 'COMPLETED' or instance.Status == 'STOPPED' or instance.Status == 'ERROR'):
                newTask = PrepareNewTask(instance, request)
                newTask.save()
                guid = newTask.GUID
                instance = Task.objects.get_queryset().filter(GUID=guid).first()
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

def PrepareNewTask(task: Task, request: requests.Request):
    t = Task(
        Idea = task.Idea,
        Station= task.Station,
        IsDebugMode = task.IsDebugMode,
        PlatformCounter = task.PlatformCounter,
        PlatformEvent = task.PlatformEvent,
        TotalIterations = task.TotalIterations,
        RegressionName = task.RegressionName,
        Tool = task.Tool,
        Platform = task.Platform,
        IsEmon = task.IsEmon,
        IsUploadResults = task.IsUploadResults,
        Splitter = task.Splitter,
        MinImpurityDecrease = task.MinImpurityDecrease,
        MaxFeatures = task.MaxFeatures,
        CreatedBy = request.user.username,
        CreatedDate = datetime.utcnow(),
        Status = "PENDING"
    )
    return t
    

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

def deleteTask(request, guids):
    list = guids.split(',')
    stationsList = []
    tasks = Task.objects.filter(GUID__in = list)
    for t in tasks:
        stationsList.append(t.Station)
    tasks.delete()

    iterations = TaskIteration.objects.filter(GUID__in = list)
    iterations.delete()
    #if there are not pending or starting jobs for the station that is being deleted
    #we can make that station active again for further use
    for stn in stationsList:
        stationsCount = Task.objects.filter(Station=stn, Status__in=['PENDING','STARTING']).count()
        if (stationsCount == 0):
            s = Station.objects.get(Name=stn)
            s.IsActive = True
            s.save()

    
    response = {
            'status': '200', 'responseText': 'success'
        }
    return JsonResponse(response)

@ldap_auth
def filterData(request):
    try:
        if (request.POST['txtFromDate'] != ''):
            fromDate = datetime.strptime(request.POST['txtFromDate'] + ' 12:00:00','%m/%d/%Y %H:%M:%S')
        
        if (request.POST['txtToDate'] != ''):
            toDate = datetime.strptime(request.POST['txtToDate'] + ' 12:00:00','%m/%d/%Y %H:%M:%S')
        else:
            toDate = datetime.strptime(request.POST['txtFromDate'] + ' 12:00:00','%m/%d/%Y %H:%M:%S')

        taskList = Task.objects.filter(CreatedDate__date__range=(fromDate, toDate))
        taskIterations = TaskIteration.objects.all().order_by("-id")
        usrs = models.User.objects.all().values('username')
        return render(request, "servicemanager/jobhistory.html", {
            "tasks": taskList, "colNames" : Task._meta.fields, "iterations" : taskIterations, "Users": usrs
        })
    except Exception as e:
        return render(request, "servicemanager/jobhistory.html", {
            "tasks": taskList, "colNames" : Task._meta.fields, "iterations" : taskIterations, "Users": usrs
        })

def filterDataNew(request, fromDate, toDate):
    try:
        if (fromDate != ''):
            fromDate = datetime.strptime(fromDate + ' 12:00:00','%m-%d-%Y %H:%M:%S')
        
        if(toDate != ''):
            toDate = datetime.strptime(toDate + ' 12:00:00','%m-%d-%Y %H:%M:%S')
        else:
            toDate = datetime.strptime(fromDate + ' 12:00:00','%m-%d-%Y %H:%M:%S')

        #taskList = Task.objects.filter(CreatedDate__date__range=(fromDate, toDate), CreatedBy = request.user.username)
        taskList = Task.objects.filter(CreatedDate__date__range=[fromDate, toDate], CreatedBy = request.user.username)
        taskListForm = []
        for i in range(len(taskList)):
            taskForm = {
            'TaskID': taskList[i].id if taskList[i].id is not None else '',
            'Station': taskList[i].Station,
            'IsDebugMode': taskList[i].IsDebugMode,
            'RegressionName': taskList[i].RegressionName,
            'Tool': taskList[i].Tool,
            'ToolEvent': taskList[i].ToolEvent if taskList[i].ToolEvent is not None else '',
            'ToolCounter': taskList[i].ToolCounter if taskList[i].ToolCounter is not None else '',
            'Platform': taskList[i].Platform,
            'IsEmon': taskList[i].IsEmon,
            'PlatformEvent': taskList[i].PlatformEvent,
            'PlatformCounter': taskList[i].PlatformCounter,
            'Idea': taskList[i].Idea,
            'IsUploadResults': taskList[i].IsUploadResults,
            'TotalIterations': taskList[i].TotalIterations,
            'Splitter': taskList[i].Splitter,
            'MinImpurityDecrease': taskList[i].MinImpurityDecrease,
            'MaxFeatures': taskList[i].MaxFeatures,
            'CreatedBy': taskList[i].CreatedBy,
            'CreatedDate': taskList[i].CreatedDate,
            'ModifiedBy': taskList[i].ModifiedBy if taskList[i].ModifiedBy is not None else '',
            'ModifiedDate': taskList[i].ModifiedDate if taskList[i].ModifiedDate is not None else '',
            'ErrorCode': taskList[i].ErrorCode if taskList[i].ErrorCode is not None else '',
            'ErrorMessage': taskList[i].ErrorMessage if taskList[i].ErrorMessage is not None else '',
            'Status': taskList[i].Status,
            'GUID': taskList[i].GUID,
            'CurrentIteration': taskList[i].CurrentIteration ,
            'IterationResult': taskList[i].IterationResult if taskList[i].IterationResult is not None else '',
            'TestResults': taskList[i].TestResults if taskList[i].TestResults is not None else '',
            'AxonLog': taskList[i].AxonLog if taskList[i].AxonLog is not None else '',
            'AzureLink': taskList[i].AzureLink if taskList[i].AzureLink is not None else '',
            'IsUserExecution': taskList[i].IsUserExecution if taskList[i].IsUserExecution is not None else '',
            'IsEowynExecution': taskList[i].IsEowynExecution if taskList[i].IsEowynExecution is not None else '',
            'ToolJson': taskList[i].ToolJson if taskList[i].ToolJson is not None else '',
            'TaskIterations': list(TaskIteration.objects.filter(GUID = str(taskList[i].GUID)).values())
            }
            taskListForm.append(taskForm)

        taskJson = json.dumps(taskListForm, cls= TaskEncoder)
        return JsonResponse({ "data": json.loads(taskJson) }, safe=False)
    except Exception as e:
        return JsonResponse({ "data": e }, safe=False)

def deleteTaskNew(request, guids):
    list = guids.split(',')
    stationsList = []
    tasks = Task.objects.filter(GUID__in = list)
    for t in tasks:
        stationsList.append(t.Station)
    tasks.delete()

    iterations = TaskIteration.objects.filter(GUID__in = list)
    iterations.delete()
    #if there are not pending or starting jobs for the station that is being deleted
    #we can make that station active again for further use
    for stn in stationsList:
        stationsCount = Task.objects.filter(Station=stn, Status__in=['PENDING','STARTING']).count()
        if (stationsCount == 0):
            s = Station.objects.get(Name=stn)
            s.IsActive = True
            s.save()
    
    taskList = Task.objects.filter(CreatedBy = request.user.username)
    taskListForm = []
    for i in range(len(taskList)):
        taskForm = {
        'TaskID': taskList[i].id if taskList[i].id is not None else '',
        'Station': taskList[i].Station,
        'IsDebugMode': taskList[i].IsDebugMode,
        'RegressionName': taskList[i].RegressionName,
        'Tool': taskList[i].Tool,
        'ToolEvent': taskList[i].ToolEvent if taskList[i].ToolEvent is not None else '',
        'ToolCounter': taskList[i].ToolCounter if taskList[i].ToolCounter is not None else '',
        'Platform': taskList[i].Platform,
        'IsEmon': taskList[i].IsEmon,
        'PlatformEvent': taskList[i].PlatformEvent,
        'PlatformCounter': taskList[i].PlatformCounter,
        'Idea': taskList[i].Idea,
        'IsUploadResults': taskList[i].IsUploadResults,
        'TotalIterations': taskList[i].TotalIterations,
        'Splitter': taskList[i].Splitter,
        'MinImpurityDecrease': taskList[i].MinImpurityDecrease,
        'MaxFeatures': taskList[i].MaxFeatures,
        'CreatedBy': taskList[i].CreatedBy,
        'CreatedDate': taskList[i].CreatedDate,
        'ModifiedBy': taskList[i].ModifiedBy if taskList[i].ModifiedBy is not None else '',
        'ModifiedDate': taskList[i].ModifiedDate if taskList[i].ModifiedDate is not None else '',
        'ErrorCode': taskList[i].ErrorCode if taskList[i].ErrorCode is not None else '',
        'ErrorMessage': taskList[i].ErrorMessage if taskList[i].ErrorMessage is not None else '',
        'Status': taskList[i].Status,
        'GUID': taskList[i].GUID,
        'CurrentIteration': taskList[i].CurrentIteration ,
        'IterationResult': taskList[i].IterationResult if taskList[i].IterationResult is not None else '',
        'TestResults': taskList[i].TestResults if taskList[i].TestResults is not None else '',
        'AxonLog': taskList[i].AxonLog if taskList[i].AxonLog is not None else '',
        'AzureLink': taskList[i].AzureLink if taskList[i].AzureLink is not None else '',
        'IsUserExecution': taskList[i].IsUserExecution if taskList[i].IsUserExecution is not None else '',
        'IsEowynExecution': taskList[i].IsEowynExecution if taskList[i].IsEowynExecution is not None else '',
        'ToolJson': taskList[i].ToolJson if taskList[i].ToolJson is not None else '',
        'TaskIterations': list(TaskIteration.objects.filter(GUID = str(taskList[i].GUID)).values())
        }
        taskListForm.append(taskForm)

    taskJson = json.dumps(taskListForm, cls= TaskEncoder)
    return JsonResponse({ "data": json.loads(taskJson) }, safe=False)
    
    


def ShowToolJson(request, fileName):
   try:
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "api", "data", fileName)
    with open(filePath, 'r') as taskfile:
        stream = io.BytesIO(str.encode(taskfile.read()))
        taskData = JSONParser().parse(stream=stream)
        return JsonResponse(taskData)
   except: 
        return JsonResponse({ 'message': 'File not found' })

def ShowJson(request):
   try:
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "api", "data", "task.json")
    with open(filePath, 'r') as taskfile:
        stream = io.BytesIO(str.encode(taskfile.read()))
        taskData = JSONParser().parse(stream=stream)
        return JsonResponse(taskData)
   except: 
        return JsonResponse({ 'message': 'File not found' })

def SendJson(request):
   requests.post("http://127.0.0.1:8000/api/posttask/", data = { "taskJSON" : request.POST['JsonData'] } )
   taskFormObj = TaskForm()
   return render(request, "servicemanager/newtask.html", {
        "taskForm": taskFormObj
    })
@csrf_exempt
def SaveToolJson(request):
   body = json.loads(request.body)

   toolJson =  body['ToolData']
   toolName = body['ToolName']
   stationName = body['StationName']
   toolObj = Tool.objects.filter(Name = toolName, StationName = stationName).first();
   toolObj.JsonFile = toolJson
   toolObj.save()
   return HttpResponse('')



@ldap_auth
def NewStation(request):
    return render(request, "servicemanager/newstation.html")
