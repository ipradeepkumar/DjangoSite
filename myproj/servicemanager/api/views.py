import os
import io
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from servicemanager.models import Task, TaskIteration
from servicemanager.api.serializers import PlatformSerializer, StationSerializer, ToolSerializer, TaskStatusSerializer, IdeaSerializer
from django.core import serializers

@api_view(['GET'])
def StationList(request):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "data", "station.json")
    with open(filePath, 'r') as stationfile:
        stream = io.BytesIO(str.encode(stationfile.read()))
        stationData = JSONParser().parse(stream=stream)
        serializer = StationSerializer(data=stationData, many=True)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


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
        # serializer = ToolSerializer(data=toolData, many=True)
        # if serializer.is_valid():
        #     return Response(serializer.validated_data)
        # else:
        #     return Response(serializer.errors)

@api_view(['GET'])
def PlatformList(request):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(dirPath, "data", "platform.json")
    with open(filePath, 'r') as platformfile:
        stream = io.BytesIO(str.encode(platformfile.read()))
        platformData = JSONParser().parse(stream=stream)
        return Response(platformData)
        # serializer = PlatformSerializer(data=platformData, many=True)
        # if serializer.is_valid():
        #     return Response(serializer.validated_data)
        # else:
        #     return Response(serializer.errors)       

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



    
     


        

    
