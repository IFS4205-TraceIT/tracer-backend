from urllib import response
from django.test import TestCase
from rest_framework.test import force_authenticate, APITestCase
from .models import (
    Users,
    Infectionhistory,
    Closecontacts,
    Contacttracers
)
from accounts.models import AuthUser
from rest_framework import status
import uuid
# Create your tests here.

class InfectionsTestCase(APITestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_superuser(username='test', email='test@test.com',password='test')

        Contacttracers(id=self.user.id).save()

        u1 = Users(id=uuid.uuid4(), nric='S1234567A', name='test1', dob='1990-01-01',email="1@1.com",phone=12345678,gender='M',address='asdsadjsa',postal_code = 'asdasd')
        u1.save()
        u2 = Users(id=uuid.uuid4(), nric='S1234568A', name='test2', dob='1990-01-02',email="1@1.com",phone=12345678,gender='M',address='asdsadjsa',postal_code = 'asdasd')
        u2.save()
        u3 = Users(id=uuid.uuid4(), nric='S1234569A', name='test3', dob='1990-01-03',email="1@1.com",phone=12345678,gender='M',address='asdsadjsa',postal_code = 'asdasd')
        u3.save()
        u4 = Users(id=uuid.uuid4(), nric='S1234560A', name='test4', dob='1990-01-04',email="1@1.com",phone=12345678,gender='M',address='asdsadjsa',postal_code = 'asdasd')
        u4.save()
        self.userid = u1.id
        i1 = Infectionhistory(user=u1, recorded_timestamp='2022-01-01')
        i1.save()
        self.infectionId = i1.id
        cc1 = Closecontacts(contacted_user=u2, infected_user=u1,infectionhistory=i1, contact_timestamp='2022-01-01', rssi = 10)
        cc1.save()
        cc2 = Closecontacts(contacted_user=u3, infected_user=u1, infectionhistory=i1, contact_timestamp='2022-01-01',rssi = 99.0)
        cc2.save()

    def test_infections(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/infections')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/infections/asdasd')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get('/api/infections/2022-01-01')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_closecontact(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/closecontacts/asdasd/asdasdas')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(f'/api/closecontacts/randomuserid/{self.infectionId}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(f'/api/closecontacts/{self.userid}/randominfectedid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(f'/api/closecontacts/{self.userid}/{self.infectionId}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_notify(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.put('/api/notify/asdasd/asdasd')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(f'/api/notify/asdasd/{self.infectionId}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(f'/api/notify/{self.userid}/asdasd')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(f'/api/notify/{self.userid}/{self.infectionId}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)






