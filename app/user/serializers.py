from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

        # this set extra settings for the field
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }
    
    def create(self, validated_data):
        ''' created user with encrypted password by using our model's create user function '''
        # validated_data is the object we got from http request
        return get_user_model().objects.create_user(**validated_data)