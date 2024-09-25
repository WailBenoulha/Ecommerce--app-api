from rest_framework import serializers
from core.models import CustomUser
from django.contrib.auth import (get_user_model,authenticate)
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','last_name','phone_number','password']


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate')
            raise serializers.ValidationError(msg,code='authorization')
        attrs['user'] = user
        return attrs