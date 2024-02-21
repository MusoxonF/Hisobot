from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .serializers import *
from .models import *
from User.serializers import *


class PhotoList(ListCreateAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class Ish_TuriView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        ish_turi = Ish_turi.objects.all()
        ser = Ish_turiSerializer(ish_turi, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = Ish_turiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class Ish_TuriDetail(APIView):
    # parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            ish_turi = Ish_turi.objects.get(id=id)
            ser = Ish_turiSerializer(ish_turi)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def patch(self, request, id):
        ish_turi = Ish_turi.objects.get(id=id)
        serializer = Ish_turiSerializer(ish_turi, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        ish_turi = Ish_turi.objects.get(id=id)
        ish_turi.delete()
        return Response(status=204)

class BolimView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        bolim = Bolim.objects.all()
        ser = BolimSerializer(bolim, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = BolimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class BolimDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            bolim = Bolim.objects.get(id=id)
            ser = BolimSerializer(bolim)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def patch(self, request, id):
        bolim = Bolim.objects.get(id=id)
        serializer = BolimSerializer(bolim, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        bolim = Bolim.objects.get(id=id)
        bolim.delete()
        return Response(status=204)

class MaxsulotView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        maxsulot = Maxsulot.objects.all()
        ser = MaxsulotSerializer(maxsulot, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = MaxsulotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class MaxsulotDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            maxsulot = Maxsulot.objects.get(id=id)
            ser = MaxsulotSerializer(maxsulot)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def patch(self, request, id):
        maxsulot = Maxsulot.objects.get(id=id)
        serializer = MaxsulotSerializer(maxsulot, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        maxsulot = Maxsulot.objects.get(id=id)
        maxsulot.delete()
        return Response(status=204)

class ProblemView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        problem = Problem.objects.all()
        ser = ProblemSerializer(problem, many=True)
        return Response(ser.data)
    
    def post(self, request):
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ProblemDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            problem = Problem.objects.get(id=id)
            ser = ProblemSerializer(problem)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def patch(self, request, id):
        problem = Problem.objects.get(id=id)
        serializer = ProblemSerializer(problem, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        problem = Problem.objects.get(id=id)
        problem.delete()
        return Response(status=204)

class HisobotView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        hisobot = Hisobot.objects.all()
        ser = HisobotGetSerializer(hisobot, many=True)
        return Response(ser.data)

    def post(self, request):
        photo = request.data.getlist('rasm', [])
        serializer = HisobotSerializer(data=request.data)
        if serializer.is_valid():
            d = serializer.save()
            for x in photo:
                s = Photo.objects.create(photo=x)
                d.rasm.add(s)
            return Response(serializer.data)
        return Response(serializer.errors)


class HisobotDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            hisobot = Hisobot.objects.get(id=id)
            ser = HisobotSerializer(hisobot)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})
    
    def patch(self, request, id):
        a = request.data.get('rasm', None)
        hisobot = Hisobot.objects.get(id=id)
        serializer = HisobotSerializer(hisobot, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if a:
                for x in a:
                    n = Photo.objects.create(photo=x)
                    hisobot.rasm.add(n)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        hisobot = Hisobot.objects.get(id=id)
        hisobot.delete()
        return Response(status=204)

        


