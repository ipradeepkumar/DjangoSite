import uuid
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from mock import MagicMock
from servicemanager.forms import TaskForm
from servicemanager.models import Station, EmonCounter, EmonEvent
from unittest.mock import Mock,patch, MagicMock
import socket
from servicemanager.views import newtask, jobhistory, StartProcess


# class LoginTestCase(TestCase):

#     def test_doLogin_InvalidLogin(self):
#         loginClient = Client()
#         loginUrl = reverse('dologin')
#         response = loginClient.post(loginUrl, {'txtUsername': 'john', 'txtPassword': 'smith'})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "servicemanager/login.html")

#     def test_doLogin_ValidLogin(self):
#         loginClient = Client()
#         loginUrl = reverse('dologin')
#         response = loginClient.post(loginUrl, {'txtUsername': 'newton', 'txtPassword': 'password'})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.content, b"id")
#         self.assertEqual(response.url, "jobhistory")
    
# class IndexTestCase(TestCase):
#     def test_Index_RedirectToLogin_IfNot_authenticated(self):
#         indexClient = Client()
#         indexUrl = reverse('index')
#         response = indexClient.get(indexUrl)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "/login?next=/")
    
#     def test_Index_Render_Index_If_Authenticated(self):
#         indexClient = Client()
#         indexClient.login(username='newton',password='password')
#         indexUrl = reverse('index')
#         response = indexClient.get(indexUrl)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "servicemanager/index.html")

# class TaskTestCase(TestCase):
#     def test_Get_NewTask(self):
#         taskClient = Client()
#         # self.user =  User.objects.create(username='newton', password='password')
#         taskClient.login(username='newton', password='password')       
#         taskUrl = reverse('newtask')
#         response = taskClient.get(taskUrl)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "servicemanager/newtask.html")
#         self.assertIsNotNone(response.context['taskForm'])
    
#     def test_Post_NewTask_InactiveStation(self):
#         taskClient = Client()
#         # self.user =  User.objects.create(username='newton', password='password')
#         self.station = Station.objects.create(StationID =1, Name='cpx-8159.fcl.com',Desc='',IsActive=False)
#         taskClient.login(username='newton', password='password')       
#         taskUrl = reverse('newtask')
#         response = taskClient.post(taskUrl, data={
#         "Stations": "cpx^cpx-8159.fcl.com",
#         "IsDebugMode": True,
#         "RegressionName": "Reg 21",
#         "Tool": "Tool 1",
#         "Platform": "cpx",
#         "IsEmon": True,
#         "PlatformEvent": "['INST_RETIRED_ANY']",
#         "PlatformCounter": "['P0C3T0']",
#         "Idea": "Idea 1",
#         "IsUploadResults": True,
#         "TotalIterations": 3,
#         "Splitter": "Random",
#         "MinImpurityDecrease": ".1",
#         "MaxFeatures": ".2",
#         "CreatedBy": "newton",
#         "CreatedDate": "2023-01-19T00:35:31.178Z",
#         "Status": "PENDING",
#         "GUID": "b0f17f6f-3f22-4a07-9fbd-b8bc0cda7ec7",
#         "CurrentIteration": 0,
#         "ToolJson": ""
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "servicemanager/newtask.html")
#         self.assertIsNotNone(response.context['taskForm'])
#         self.assertEqual(response.context['message'], 'Station is already in use.')

#     def test_Post_NewTask_ActiveStation(self):
#         taskClient = Client()
#         # self.user =  User.objects.create(username='newton', password='password')
#         self.station = Station.objects.create(StationID =1, Name='cpx-8159.fcl.com',Desc='',IsActive=True)
#         taskClient.login(username='newton', password='password')       
#         taskUrl = reverse('newtask')
#         response = taskClient.post(taskUrl, data={
#         "Stations": "cpx^cpx-8159.fcl.com",
#         "IsDebugMode": True,
#         "RegressionName": "Reg 21",
#         "Tool": "Tool 1",
#         "Platform": "cpx",
#         "IsEmon": True,
#         "PlatformEvent": "['INST_RETIRED_ANY']",
#         "PlatformCounter": "['P0C3T0']",
#         "Idea": "Idea 1",
#         "IsUploadResults": True,
#         "TotalIterations": 3,
#         "Splitter": "Random",
#         "MinImpurityDecrease": ".1",
#         "MaxFeatures": ".2",
#         "CreatedBy": "newton",
#         "CreatedDate": "2023-01-19T00:35:31.178Z",
#         "Status": "PENDING",
#         "GUID": "b0f17f6f-3f22-4a07-9fbd-b8bc0cda7ec7",
#         "CurrentIteration": 0,
#         "ToolJson": ""
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "jobhistory")




class NewTaskViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock(username="Test")

   
    @patch("servicemanager.models.EmonEvent.objects.filter", return_value=[{'Name':'event1'}, {'Name':'event2'}])
    @patch("servicemanager.models.EmonCounter.objects.filter", return_value=[{'Name':'counter1'}, {'Name':'counter2'}])
    @patch("servicemanager.models.Station.objects.get", return_value=MagicMock(IsActive=True))
    @patch("django.contrib.auth.decorators.user_passes_test")
    def test_newtask_POST(self, mock_ldap_auth, mock_station, mock_emoncounter, mock_emonevent):

        # mock the user_passes_test decorator
        mock_ldap_auth.return_value = True

        request = self.factory.post(reverse("newtask"), data={
            "Idea": "test idea",
            "Stations": "test_platform^test_station",
            "DebugMode": True,
            "EmonCounters": [1, 2],
            "EmonEvents": [3, 4],
            "TotalIterations": 10,
            "RegressionName": "test regression",
            "ToolName": "test tool",
            "IsEmon": True,
            "IsUploadResult": True,
            "Splitter": "test splitter",
            "MinImpurityDecrease": 0.1,
            "MaxFeatures": 20,
            "ToolJson": "{'key': 'value'}",
            "CreatedBy": "Test"
        })
        request.user = self.user
        response = newtask(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "jobhistory")
        mock_station.assert_called_once_with(Name="test_station")
        mock_emoncounter.assert_called_once_with(EmonCounterID__in=['1', '2'])
        mock_emonevent.assert_called_once_with(EmonEventID__in=['3', '4'])

    @patch("socket.gethostname", return_value="testhost")
    @patch("socket.gethostbyname", return_value="192.168.1.1")
    @patch("django.contrib.auth.decorators.user_passes_test")
    def test_newtask_GET(self, mock_ldap_auth, mock_gethostbyname, mock_gethostname):

        # mock the user_passes_test decorator
        mock_ldap_auth.return_value = True

        request = self.factory.get(reverse("newtask"))
        request.user = self.user
        response = newtask(request)

        self.assertEqual(response.status_code, 200)
        mock_gethostbyname.assert_called_once_with('testhost')
        mock_gethostname.assert_called()

class JobHistoryTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock(username="Test")    

    
    @patch("servicemanager.models.TaskIteration.objects.all", return_value=[{'id':1, 'TaskID':1, 'GUID':'b0f17f6f-3f22-4a07-9fbd-b8bc0cda7ec7', 'Iteration':3, 'JSONData':''}, {'id':2, 'TaskID':2, 'GUID':'b0f17f6f-3f22-4a07-9fbd-b8bc0cday657', 'Iteration':0, 'JSONData':''}])
    @patch("servicemanager.models.Task.objects.all", return_value=[{'TaskID':1, 'Station':'cpx-i5-47l', 'IsDebugMode':'true', 'RegressionName':'Reg 1','Tool':'Tool 1', 'ToolEvent':'["1","3"]', 'Platform':'Platform 1','Idea':'Idea 1'}, {'TaskID':2, 'Station':'cpx-i7-47l', 'IsDebugMode':'true', 'RegressionName':'Reg 2','Tool':'Tool 2', 'ToolEvent':'["1","4"]', 'Platform':'Platform 2','Idea':'Idea 2'}])
    @patch("django.contrib.auth.decorators.user_passes_test")
    def test_jobhistory_get(self, mock_ldap_auth, mock_task, mock_taskIteration):
        mock_ldap_auth.return_value = True

        request = self.factory.get(reverse("jobhistory"))
        request.user = self.user
        response = jobhistory(request)

        self.assertEqual(response.status_code, 200)

class ProcessTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock(username="Test")
        self.guid = uuid.uuid1()

    @patch("servicemanager.models.TaskExecutionLog.objects", return_value=MagicMock(TaskID=1, Status="COMPLETED"))
    @patch("servicemanager.models.Station.objects.get", return_value=MagicMock(Name='cpx-i5-47l', IsActive=True))
    @patch("servicemanager.models.Task.objects")
    @patch("django.contrib.auth.decorators.user_passes_test")
    def test_startprocess_post(self, mock_ldap_auth, mock_task, mock_station, mock_taskexecution):
        mock_ldap_auth.return_value = True
        
        mock_task.return_value = [MagicMock(TaskID=1, GUID=self.guid,Status='PENDING',Station='Station 1'),MagicMock(TaskID=2, GUID=uuid.uuid1(),Status='COMPLETED',Station='Station 2')]
        mock_task.return_value[0].Status = "PENDING"
        request = self.factory.get("startprocess/", data={'GUID':self.guid, 'userExecution':1, 'eowynExecution':1})
        request.user = self.user
        response = StartProcess(request, GUID=self.guid, userExecution=1, eowynExecution=1)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.__contains__(b"error"))



