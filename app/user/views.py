from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

class CreateUserView(generics.CreateAPIView):
    ''' create a new user in the system '''
    # this defines the serializer correlated with this View and
    # all request will pass to serializer
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    ''' create a new auth token for user '''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    