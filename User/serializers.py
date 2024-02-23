from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user = User.objects.get(username=self.user.username)
        data['status'] = user.status
        data['id'] = user.id
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'gender', 'phone', 'image')
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
        fields = ('id', 'gender', 'name', 'last_name', 'image', 'phone', 'ish_turi', 'xodim_id', 'bolimi')
        read_only_fields = ('created', 'updated')

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.image = validated_data.get('image', instance.image)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.ish_turi = validated_data.get('ish_turi', instance.ish_turi)
        instance.xodim_id = validated_data.get('xodim_id', instance.xodim_id)
        instance.bolimi = validated_data.get('bolimi', instance.bolimi)
        instance.save()
        return instance
        
        
class Ish_turiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ish_turi
        fields = ('id', 'ish_name', 'ish_id')

class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = ('id', 'name', 'bolim_id', 'user')