from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        ''' test create user with the correct payload successful '''

        payload = {
            "email": 'test123@gmail.com',
            "password": 'testpass',
            "name": 'Test Name'
        }
        
        # APIClient will make a post request to create user url
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print(res.data)
        # get the user object we jsust created and make sure the passwords is right
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        '''Testing created the user already in will be failed'''

        payload = {
            "email": 'test123@gmail.com',
            "password": 'testpass',
            "name": 'Test Name'
        }
        # crate the user first
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        ''' pass must more than 5 '''
        payload = {
            "email": 'test123@gmail.com',
            "password": 'test',
            "name": 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # confirm user never created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
