from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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

    # token is only for already user for the testing api purpose
    def test_create_token_for_user(self):
        ''' Test that a token is created for the user '''
        payload = {
            "email": 'test123@gmail.com',
            "password": 'testpass',
            "name": 'Test'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # then we expect the resposnse includes a token
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        ''' Test that token is not created if invalid credentials are given '''
        # firstly created a valid user
        create_user(email='test123@gmail.com', password='testpass', name='Test')

        # then created token with wrong credentials
        payload = {
            "email": 'test123@gmail.com',
            "password": 'wrong',
            "name": 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dont_create_token_no_user(self):
        ''' Test that token is not created if user is not existed '''
        payload = {
            "email": 'test123@gmail.com',
            "password": 'testpass',
            "name": 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        ''' test that email and password are required '''
        res = self.client.post(TOKEN_URL, {"email": 'test123@gmail.com', "password": ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # TEST FOR: ME_URL
    def test_retrieve_user_unauthorized(self):
        ''' Test that authentication is required for users when they retrieve the user information'''
        res = self.client.get(ME_URL)
        # since user havent loged in so it must ben unauthorized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    ''' Test apis that require the authentication ''' 

    def setUp(self):
        # crate the user first
        self.user = create_user(
            email='test123@gmail.com',
            password='testpass',
            name='Test Name')
        self.client = APIClient()
        # so any request made the by test client will be authenticated by the user we just created
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        ''' Test retrieve profile for logged in user '''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })
    
    def test_post_me_not_allowed(self):
        ''' since the update should be done through: PUT or PATCH and POST should be used for create new object '''
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        ''' test for updating the user profile for authenticated user '''
        payload = {
            "password": 'newtestpass',
            "name": 'New Test Name'
        }
        res = self.client.patch(ME_URL, payload)
        #https://docs.djangoproject.com/en/3.1/ref/models/instances/#django.db.models.Model.refresh_from_db
        # Model object's refresh_from_db mehtod will load everything from db
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        #https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
        self.assertTrue(self.user.check_password(payload['password']))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

