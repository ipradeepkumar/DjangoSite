from django.urls import include, path
from rest_framework import routers
from servicemanager.api.views import StationList, ToolList, ToolEventList
#from servicemanager.api.views import UserViewSet, GroupViewSet

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# path('', include(router.urls)),
urlpatterns = [
    path('stations/', StationList, name='station_list'),
    path('tools/', ToolList, name='tool_list'),
    path('toolevents/', ToolEventList, name='tool_event_list'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]