from django.urls import path
from . import views


urlpatterns  = [
    path("", views.index, name="index"),
    path("newtask", views.newtask, name="newtask"),
    path("jobhistory", views.jobhistory, name="jobhistory"),
    path("jobhistory/<int:pk>", views.TaskDetailView.as_view(), name="jobhistory_detail")
]