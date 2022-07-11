from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "servicemanager/index.html")

def newtask(request):
    return render(request, "servicemanager/newtask.html")

def jobhistory(request):
    pass


def jobhistory_detail(request, jobid):
    pass
