from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns  = [
    path("", views.index, name="index"),
    path("newtask", views.newtask, name="newtask"),
    path("jobhistory", views.jobhistory, name="jobhistory"),
    path("jobhistory/<int:id>", views.jobhistory_detail, name="jobhistory_detail"),
    path("testldap", views.test_ldap, name="testldap"),
    path("login", views.doLogin, name="dologin"),
    path("logout", views.customlogout, name="logout")
    

]