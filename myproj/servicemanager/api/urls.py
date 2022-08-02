from django.urls import include, path
from rest_framework import routers
from servicemanager.api.views import StationList, ToolList, ToolEventList, PlatformList, TaskStatusList, IdeaList


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# path('', include(router.urls)),
urlpatterns = [
    path('stations/', StationList, name='station_list'),
    path('tools/', ToolList, name='tool_list'),
    path('toolevents/<int:toolid>', ToolEventList, name='tool_event_list'),
    path('platforms/', PlatformList, name='platform_list'),
    path('ideas/', IdeaList, name='idea_list'),
    path('taskstatuses/', TaskStatusList, name='taskstatus_list'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]