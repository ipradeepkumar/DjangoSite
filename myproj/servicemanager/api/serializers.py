from dataclasses import fields
from platform import platform
from pyexpat import model
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from servicemanager.models import Station, Tool, ToolEvent, ToolCounter, Platform, EmonCounter, EmonEvent, Idea, TaskStatus, Task, TaskIteration


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = '__all__'

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'

class EmonCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmonCounter
        fields = ['EmonCounterID', 'Name']

class EmonEventSerializer(serializers.ModelSerializer):
    emoncounters = EmonCounterSerializer(many=True)
    class Meta:
        model = EmonEvent
        fields = ['EmonEventID', 'Name', 'emoncounters']
    def create(self, validated_data):
        emoncounters_data = validated_data.pop('emoncounters')
        emonevent = EmonEvent.objects.create(**validated_data)
        for emoncounter_data in emoncounters_data:
            EmonCounter.objects.create(EmonEvent=emonevent, **emoncounter_data)
        return emonevent

class PlatformSerializer(serializers.ModelSerializer):
    emonevents = EmonEventSerializer(many=True)
    class Meta:
        model = Platform
        fields=['PlatformID', 'Name', 'emonevents']
    
    def create(self, validated_data):
        emonevents_data = validated_data.pop('emonevents')
        platform = Platform.objects.create(**validated_data)
        for emonevent_data in emonevents_data:
            EmonEvent.objects.create(Platform=platform, **emonevent_data)
        return platform


class ToolCounterSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ToolCounter
        fields = ['ToolCounterID', 'Name']
        extra_kwargs = {
            'ToolCounterID': {
                'validators': []
            }
        }
class ToolEventSerializer(serializers.ModelSerializer):
    
    toolcounterevents = ToolCounterSerializer(many = True)

    class Meta:
        model = ToolEvent
        fields = ['ToolEventID', 'Name', 'toolcounterevents']
        extra_kwargs = {
            'ToolEventID': {
                'validators': []
            }
        }
    
    def create(self, validated_data):
        toolcounterevents_data = validated_data.pop('toolcounterevents')
        toolevent = ToolEvent.objects.create(**validated_data)
        for toolcounterevent_data in toolcounterevents_data:
            ToolCounter.objects.create(ToolEvent=toolevent, **toolcounterevent_data)
        return toolevent


class ToolSerializer(serializers.ModelSerializer):
    
    toolevents = ToolEventSerializer(many = True)

    class Meta:
        model = Tool
        fields = ['ToolID', 'Name', 'toolevents']
        extra_kwargs = {
            'ToolID': {
                'validators': []
            }
        }
    
    def create(self, validated_data):
        toolevents_data = validated_data.pop('toolevents')
        tool = Tool.objects.create(**validated_data)
        for toolevent_data in toolevents_data:
            ToolEvent.objects.create(Tool=tool, **toolevent_data)
        return tool

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('GUID','TotalIterations', 'Status','CurrentIteration','TestResults','AxonLog','IterationResult','AzureLink')

class TaskIterationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskIteration
        fields = ('TaskID', 'GUID', 'JSONData', 'CreatedData', 'CreatedBy')