from django.urls import include, path
from rest_framework import routers
from servicemanager.api.views import StationList, ToolList, GetToolNames, GetToolJson, ToolEventList, PlatformList, TaskStatusList, IdeaList, GetJobJson, GetIterationJson, GetPlatformEvents, GetPlatformCounters


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# path('', include(router.urls)),
urlpatterns = [
    path('stations/', StationList, name='station_list'),
    path('tools/', ToolList, name='tool_list'),
    path('toolByStation/<stationName>', GetToolNames, name='tool_names'),
    path('toolJson/<toolName>', GetToolJson ,name='toolJson'),
    path('toolevents/<int:toolid>', ToolEventList, name='tool_event_list'),
    path('platforms/', PlatformList, name='platform_list'),
    path('event/<stationName>', GetPlatformEvents, name='platform_events'),
    path('counter/<eventID>', GetPlatformCounters, name='platform_counter'),
    path('ideas/', IdeaList, name='idea_list'),
    path('taskstatuses/', TaskStatusList, name='taskstatus_list'),
    path('getjobjson/<int:id>', GetJobJson, name='get_job_json'),
    path('getiterationjson/<int:iterationID>/<int:taskID>', GetIterationJson, name='get_iteration_json'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]