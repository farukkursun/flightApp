from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [validators.UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(
        required = True,
        write_only =True,
        validators = [validate_password]
        )
    password2 = serializers.CharField(
        required = True,
        write_only = True,
        validators = [validate_password]
        )


    class Meta:
        model = User
        exclude= [
            "last_login",
            "groups",
            "is_active",
            "date_joined",
            "user_permissions",

        ]

    #override
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'message': 'password are not same'})
        return attrs

    #override
    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
             


#############################

from dj_rest_auth.serializers import TokenSerializer

class CustomTokenSerializer(TokenSerializer):

    user = RegisterSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ['key', 'user']



      
