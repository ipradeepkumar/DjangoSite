import os
import io
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from servicemanager.models import Task, TaskIteration, EmonCounter, EmonEvent, Platform, Station, Tool
from servicemanager.api.serializers import PlatformSerializer, StationSerializer, ToolSerializer, TaskStatusSerializer, IdeaSerializer
from django.core import serializers


@api_view(['GET'])
def StationList(request):
    #pendingStationList = Task.objects.filter(Status__in=['COMPLETED','STOPPED']).values_list("Station").distinct()
    #stations = Station.objects.filter(Name__in=pendingStationList)

    stations = Station.objects.filter(IsActive__in=[True, None])
    serialized_obj = serializers.serialize('json', stations)
    return HttpResponse(serialized_obj, content_type="application/json")
    # dirPath = os.path.dirname(os.path.realpath(__file__))
    # filePath = os.path.join(dirPath, "data", "station.json")
    # with open(filePath, 'r') as stationfile:
    #     stream = io.BytesIO(str.encode(stationfile.read()))
    #     stationData = JSONParser().parse(stream=stream)
    #     serializer = StationSerializer(data=stationData, many=True)
    #     if serializer.is_valid():
    #         return Response(serializer.validated_data)
    #     else:
    #         return Response(serializer.errors)


@api_view(['GET'])
def ToolList(request):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "data", "tool.json")
    with open(filePath, 'r') as toolfile:
        stream = io.BytesIO(str.encode(toolfile.read()))
        toolData = JSONParser().parse(stream=stream)
        return Response(toolData)
        #serializer = ToolSerializer(data=toolData, many=True)
        #if serializer.is_valid():
        #else:
            #return Response(serializer.errors)


@api_view(['GET'])
def ToolEventList(request, toolid):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "data", "tool.json")
    with open(filePath, 'r') as tooleventfile:
        stream = io.BytesIO(str.encode(tooleventfile.read()))
        toolData = JSONParser().parse(stream=stream)
        return Response(toolData)

@api_view(['GET'])
def PlatformList(request):
        platformData = Platform.objects.all()
        serialized_obj = serializers.serialize('json', platformData)
        return HttpResponse(serialized_obj, content_type="application/json")

@api_view(['GET'])
def IdeaList(request):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "data", "idea.json")
    with open(filePath, 'r') as ideafile:
        stream = io.BytesIO(str.encode(ideafile.read()))
        ideaData = JSONParser().parse(stream=stream)
        serializer = IdeaSerializer(data=ideaData, many=True)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)    

@api_view(['GET'])
def TaskStatusList(request):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "data", "taskstatus.json")
    with open(filePath, 'r') as taskstatusfile:
        stream = io.BytesIO(str.encode(taskstatusfile.read()))
        taskStatusData = JSONParser().parse(stream=stream)
        serializer = TaskStatusSerializer(data=taskStatusData, many=True)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)  
        
@api_view(['GET'])
def GetJobJson(request, id):
    task = Task.objects.get(pk = id)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', [ task ])
    return Response(serialized_obj)

@api_view(['GET'])
def GetIterationJson(request, iterationID, taskID):
    iterationData = TaskIteration.objects.get_queryset().filter(Iteration=iterationID, TaskID=taskID).first()
    # assuming obj is a model instance
    #serialized_obj = serializers.serialize('json', [ task ])
    return Response(iterationData.JSONData)

@api_view(['GET'])
def GetPlatformEvents(request, stationName):
    platformEventData = EmonEvent.objects.filter(Station__Name = stationName)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', platformEventData)
    return HttpResponse(serialized_obj, content_type="application/json")

@api_view(['GET'])
def GetPlatformCounters(request, eventID):
    list= eventID.split(",")
    emonCounterData = EmonCounter.objects.filter(EmonEvent__EmonEventID__in = list)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', emonCounterData)
    return HttpResponse(serialized_obj, content_type="application/json")

@api_view(['GET'])
def GetToolNames(request, stationName):
    toolData = Tool.objects.filter(StationName = stationName)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', toolData)
    return HttpResponse(serialized_obj, content_type="application/json")

@api_view(['GET'])
def GetToolJson(request, toolName):
    toolData = Tool.objects.filter(Name = toolName)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', toolData)
    return HttpResponse(serialized_obj, content_type="application/json")







    
     


        

    
