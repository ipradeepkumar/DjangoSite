from django.test import TestCase, Client
from django.urls import reverse
from servicemanager.models import Task
from servicemanager.forms import TaskForm
# Create your tests here.

class TestTaskForm(TestCase):
    def test_task_is_invalid(self):
        form = TaskForm(data={
        "TaskID": None,
        "Station": "cpx-8159.fcl.com",
        "IsDebugMode": True,
        "RegressionName": "Reg 21",
        "Tool": "Tool 1",
        "ToolEvent": None,
        "ToolCounter": None,
        "Platform": "cpx",
        "IsEmon": True,
        "PlatformEvent": "['INST_RETIRED_ANY']",
        "PlatformCounter": "['P0C3T0']",
        "Idea": "Idea 1",
        "IsUploadResults": True,
        "TotalIterations": 3,
        "Splitter": "Random",
        "MinImpurityDecrease": ".1",
        "MaxFeatures": ".2",
        "CreatedBy": "newton",
        "CreatedDate": "2023-01-19T00:35:31.178Z",
        "ModifiedBy": None,
        "ModifiedDate": None,
        "ErrorCode": None,
        "ErrorMessage": None,
        "Status": "PENDING",
        "GUID": "b0f17f6f-3f22-4a07-9fbd-b8bc0cda7ec7",
        "CurrentIteration": 0,
        "IterationResult": None,
        "TestResults": None,
        "AxonLog": None,
        "AzureLink": None,
        "IsUserExecution": None,
        "IsEowynExecution": None,
        "ToolJson": ""
        }
        )
        self.assertTrue(form.is_valid())

   
 