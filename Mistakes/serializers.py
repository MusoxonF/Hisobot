from rest_framework import serializers

from .models import *
from User.serializers import UserSerializer, XodimSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'photo')


class MaxsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maxsulot
        fields = ('id', 'name','maxsulot_id')


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'xato_id', 'problem_name')


class HisobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hisobot
        fields = ('id', 'xodim', 'user', 'problem', 'rasm', 'files', 'izoh', 'created', 'updated','maxsulot', 'xato_soni', 'butun_soni', 'ish_vaqti')

    def update(self, instance, validated_data):
        instance.xodim = validated_data.get('xodim', instance.xodim)
        instance.user = validated_data.get('user', instance.user)
        instance.problem = validated_data.get('problem', instance.problem)
        # instance.rasm = validated_data.get('rasm', instance.rasm)
        instance.files = validated_data.get('files', instance.files)
        instance.izoh = validated_data.get('izoh', instance.izoh)
        instance.maxsulot = validated_data.get('maxsulot', instance.maxsulot)
        instance.xato_soni = validated_data.get('xato_soni', instance.xato_soni)
        instance.butun_soni = validated_data.get('butun_soni', instance.butun_soni)
        instance.ish_vaqti = validated_data.get('ish_vaqti', instance.ish_vaqti)
        instance.save()
        return instance


class HisobotGetSerializer(serializers.ModelSerializer):
    xodim = XodimSerializer()
    user = UserSerializer()
    problem = ProblemSerializer()
    maxsulot = MaxsulotSerializer()
    rasm = PhotoSerializer(many=True)
    class Meta:
        model = Hisobot
        fields = ('id', 'xodim', 'user', 'problem', 'files', 'izoh', 'created', 'updated','maxsulot', 'xato_soni', 'butun_soni', 'ish_vaqti', 'rasm')