from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
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


class AuthTokenSerializer(serializers.Serializer):
    ''' Serializer for the user authentication object '''

    email = serializers.CharField()
    password= serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # custom validators: https://www.django-rest-framework.org/api-guide/validators/#optional-fields
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        
        attrs['user'] = user
        return attrs




