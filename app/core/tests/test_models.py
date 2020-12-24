from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='qingyuan@test.com', password="test123"):
    '''create a sample user'''
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    def test_create_user_with_email_successfull(self):
        """Testing create a new user with email successful"""

        email = "qingyuan@georgetown.edu"
        password = "testPasss1234566"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, "123")
         
        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Testing the new user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test1234")

    def test_create_new_superuser(self):
        """Test creating new superuser"""

        user = get_user_model().objects.create_superuser(
            email="qingyuan@test.com",
            password="test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
    
