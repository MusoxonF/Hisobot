from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user = User.objects.get(username=self.user.username)
        data['status'] = user.status
        data['id'] = user.id
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        # data2 = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # data2 = attrs.get('refresh')
        data['refresh'] = attrs.get('refresh') 
        # user = User.objects.get(username=self.user.username)
        # data['status'] = user.status
        # data['id'] = user.id
        # return (data, f'refresh: {data2}')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name',  'photo', 'gender', 'phone', 'status', 'gender')
        write_only_fields = ('password')
        extra_kwargs = {
            'password': {
                'write_only': True,
               'style': {'input_type': 'password'}
            }
        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user


class XodimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xodim
        fields = ('id', 'first_name', 'last_name', 'photo', 'phone', 'ish_turi', 'id_raqam', 'gender', 'bulimi')
        read_only_fields = ('created', 'updated')

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.ish_turi = validated_data.get('ish_turi', instance.ish_turi)
        instance.id_raqam = validated_data.get('id_raqam', instance.id_raqam)
        instance.bulimi = validated_data.get('bulimi', instance.bulimi)
        instance.save()
        return instance
        
        
class Ish_turiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ish_turi
        fields = ('id', 'name', 'ish_id')

class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = ('id', 'name', 'bulim_id', 'user')