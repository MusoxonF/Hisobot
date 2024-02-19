from rest_framework import serializers
from .models import *


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
        user = super(UserSerializers, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user


class XodimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xodim
        fields = ('id', 'gender', 'name', 'last_name', 'image', 'phone', 'ish_turi', 'xodim_id', 'bolimi')
        read_only_fields = ('created', 'updated')
        
class Ish_turiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ish_turi
        fields = ('id', 'ish_name')

class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = ('id', 'name', 'bolim_id', 'user')