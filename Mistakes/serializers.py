from rest_framework import serializers

from .models import *
from User.serializers import UserSerializer, XodimSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class MaxsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maxsulot
        fields = ('name','maxsulot_id')


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('xato_id', 'problem_name')


class HisobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hisobot
        fields = ('xodim', 'user', 'problem', 'rasm', 'files', 'izoh', 'created', 'updated','maxsulot', 'xato_soni', 'butun_soni', 'ish_vaqti')


class HisobotGetSerializer(serializers.ModelSerializer):
    xodim = XodimSerializer()
    user = UserSerializer()
    problem = ProblemSerializer()
    maxsulot = MaxsulotSerializer()
    photo = PhotoSerializer(many=True)
    class Meta:
        model = Hisobot
        fields = ('id', 'xodim', 'user', 'problem', 'files', 'izoh', 'created', 'updated','maxsulot', 'xato_soni', 'butun_soni', 'ish_vaqti', 'photo')