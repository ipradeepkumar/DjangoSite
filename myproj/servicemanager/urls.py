from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns  = [
    path("", views.index, name="index"),
    path("newtask", views.newtask, name="newtask"),
    path("jobhistory", views.jobhistory, name="jobhistory"),
    path("jobhistory/<int:id>", views.jobhistory_detail, name="jobhistory_detail"),
    path("testldap", views.test_ldap, name="testldap"),
    path("login", views.doLogin, name="dologin"),
    path("logout", views.customlogout, name="logout"),
    path("startprocess/<GUID>/<int:userExecution>/<int:eowynExecution>", views.StartProcess, name="startprocess")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)