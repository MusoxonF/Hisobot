from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, JSONParser


class SignUpView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        user = User.objects.all()
        ser = UserSerializer(user, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class SignUpDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            ser = UserSerializer(user)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def patch(self, request, id):
        user = User.objects.get(id=id)
        ser = UserSerializer(user, data = request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response({'message':'user o\'chirildi'})


class XodimView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        xodim = Xodim.objects.all()
        ser = XodimSerializer(xodim, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = XodimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class XodimDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            xodim = Xodim.objects.get(id=id)
            ser = XodimSerializer(xodim)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def patch(self, request, id):
        a = request.data.get('ish_turi', None)
        xodim = Xodim.objects.get(id=id)
        ser = XodimSerializer(xodim, data = request.data, partial=True)
        if ser.is_valid():
            s = ser.save()
            if a:
                validated_data.pop('ish_turi')
                for x in a:
                    s.ish_turi.add(x)
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, id):
        xodim = Xodim.objects.get(id=id)
        xodim.delete()
        return Response({'message':'xodim o\'chirildi'})

    