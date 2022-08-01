from pyexpat import model
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from servicemanager.models import Station, Tool, ToolEvent, ToolCounter


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'
    # StationID = serializers.IntegerField()
    # Name = serializers.CharField(max_length=250)
    # Desc = serializers.CharField(max_length=500)

    # def create(self, validated_data):
    #     return Station.objects.create(**validated_data)

class ToolCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolCounter
        fields = '__all__'

class ToolEventSerializer(serializers.ModelSerializer):
    toolcounterevents = ToolCounterSerializer(many = True)
    class Meta:
        model = ToolEvent
        fields = ['ToolEventID', 'Name', 'toolcounterevents']
    
    def create(self, validated_data):
        toolcounterevents_data = validated_data.pop('toolcounterevents')
        toolevent = ToolEvent.objects.create(**validated_data)
        for toolcounterevent_data in toolcounterevents_data:
            ToolCounter.objects.create(ToolEvent=toolevent, **toolcounterevent_data)
        return toolevent

    # ToolEventID = serializers.IntegerField()
    # Name = serializers.CharField(max_length=150)

    # def create(self, validated_data):
    #     return ToolEvent.objects.create(**validated_data) 

class ToolSerializer(serializers.ModelSerializer):
    toolevents = ToolEventSerializer(many = True)

    class Meta:
        model = Tool
        fields = ['ToolID', 'Name', 'toolevents']
    
    def create(self, validated_data):
        toolevents_data = validated_data.pop('toolevents')
        tool = Tool.objects.create(**validated_data)
        for toolevent_data in toolevents_data:
            ToolEvent.objects.create(Tool=tool, **toolevent_data)
        return tool

    # ToolID = serializers.IntegerField()
    # Name = serializers.CharField(max_length=150)
     
    # def create(self, validated_data):
    #     return Tool.objects.create(**validated_data)




       
