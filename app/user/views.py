from user.serializers import UserSerializer
from rest_framework import generics

class CreateUserView(generics.CreateAPIView):
    ''' create a new user in the system '''

    # this defines the serializer correlated with this View and
    # all request will pass to serializer
    serializer_class = UserSerializer
