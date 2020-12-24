from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers

# Create your views here.

# so GenericViewSet itself doesnt have the actions so it need to add `mixins.ListModelMixin` to 
# bring the `list` operation
class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    ''' manage tags in the database '''
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    # queryset(must): The queryset that should be used for returning objects from this view
    queryset = Tag.objects.all()
    # serializer_class(must): The serializer class that should be used for validating and deserializing input, and for serializing output
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        ''' return objects to the current authenticated user only '''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        ''' create a new tag '''
        serializer.save(user=self.request.user)
    


