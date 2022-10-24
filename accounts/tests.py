from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .views import RegistrationAPIView
from .models import AuthUser

# Create your tests here.
class RegistrationTest(TestCase):
    databases = {'default', 'main_db'}
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_registration_incomplete(self):
        """Test registration with incomplete data."""
        res = self.client.post('/auth/register', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.post('/auth/register', {
            'username': 'test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'username': 'test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'phone_number': 'test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_invalid(self):
        """Test registration with invalid data."""
        # Invalid email
        res = self.client.post('/auth/register', {
            'email': 'test',
            'username': 'test',
            'phone_number': 'test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Password too short
        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'username': 'test',
            'phone_number': 'test',
            'password': 'test'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Password too simple
        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'username': 'test',
            'phone_number': 'test',
            'password': 'testtest'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_success(self):
        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'username': 'test',
            'phone_number': 'test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AuthUser.objects.count(), 1)
        self.assertEqual(AuthUser.objects.get().username, 'test')

class LoginTest(TestCase):
    databases = {'default', 'main_db'}
    def setUp(self) -> None:
        self.client = APIClient()
        res = self.client.post('/auth/register', {
            'email': 'test@test.test',
            'username': 'tracer',
            'phone_number': 'test',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AuthUser.objects.count(), 1)
        self.assertEqual(AuthUser.objects.get().username, 'tracer')
        # Create user with no tracer profile
        user = AuthUser.objects.create_user('test', 'test@test.test', '1qwer$#@!')
        user.phone_number = 'test'
        user.save()
    
    def test_login_incomplete(self):
        """Test login with incomplete data."""
        res = self.client.post('/auth/login', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.post('/auth/login', {
            'username': 'test'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.post('/auth/login', {
            'password': 'testtest'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_invalid(self):
        """Test login with invalid data."""
        res = self.client.post('/auth/login', {
            'username': 'a',
            'password': 'test'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        res = self.client.post('/auth/login', {
            'username': 'tracer',
            'password': 'test'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.post('/auth/login', {
            'username': 'test',
            'password': 'test'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_valid(self):
        """Test login with valid data."""
        res = self.client.post('/auth/login', {
            'username': 'tracer',
            'password': '1qwer$#@!'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
