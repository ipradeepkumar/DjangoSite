import uuid
from servicemanager.views import index
from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestServiceUrls(SimpleTestCase):
    
    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).view_name,'index')

    def test_newtask_is_resolved(self):
        url = reverse('newtask')
        self.assertEquals(resolve(url).view_name,'newtask')

    def test_jobhistory_is_resolved(self):
        url = reverse('jobhistory')
        self.assertEquals(resolve(url).view_name,'jobhistory')
    
    def test_login_is_resolved(self):
        url = reverse('dologin')
        self.assertEquals(resolve(url).view_name,'dologin')
    
    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).view_name,'logout')

    def test_startprocess_is_resolved(self):
        url = reverse('startprocess', args=[uuid.uuid1(),1,1])
        self.assertEquals(resolve(url).view_name,'startprocess')
    
    def test_deletetask_is_resolved(self):
        url = reverse('deleteTask', args=[1])
        self.assertEquals(resolve(url).view_name,'deleteTask')

    def test_filterdata_is_resolved(self):
        url = reverse('filterData')
        self.assertEquals(resolve(url).view_name,'filterData')
    
    def test_showjson_is_resolved(self):
        url = reverse('ShowJson')
        self.assertEquals(resolve(url).view_name,'ShowJson')
    
    def test_sendjson_is_resolved(self):
        url = reverse('SendJson')
        self.assertEquals(resolve(url).view_name,'SendJson')
    
    def test_showtooljson_is_resolved(self):
        url = reverse('ShowToolJson', args=['testfile.json'])
        self.assertEquals(resolve(url).view_name,'ShowToolJson')