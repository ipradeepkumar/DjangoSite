from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns  = [
    path("", views.index, name="index"),
    path("newtask", views.newtask, name="newtask"),
    path("jobhistory", views.jobhistory, name="jobhistory"),
    #path("jobhistory/<int:id>", views.jobhistory_detail, name="jobhistory_detail"),
    path("testldap", views.test_ldap, name="testldap"),
    path("login", views.doLogin, name="dologin"),
    path("logout", views.customlogout, name="logout"),
    path("startprocess/<GUID>/<int:userExecution>/<int:eowynExecution>", views.StartProcess, name="startprocess"),
    path("deleteTask/<guids>", views.deleteTask, name="deleteTask"),
    path("filterData/", views.filterData, name="filterData"),
    path("ShowJson", views.ShowJson, name="ShowJson"),
    path("SendJson", views.SendJson, name="SendJson"),
    path('ShowToolJson/<fileName>', views.ShowToolJson ,name="ShowToolJson"),
    path('NewStation', views.NewStation ,name="newstation"),
    path('SaveToolJson', views.SaveToolJson  ,name="SaveToolJson")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)