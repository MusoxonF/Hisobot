from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from django.db.models import Sum, Max, Min, Count, F, Q, Avg
from .serializers import *
from .models import *
from User.serializers import *
from User.models import *


class PhotoList(ListCreateAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoEditView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def patch(self, request, id):
        photo = Photo.objects.get(id=id)
        rasm = request.data.get('photo')
        photo.photo = rasm
        photo.save()
        return Response({'message': 'successfully'})

    def get(self, request, id):
        try:
            photo = Photo.objects.get(id=id)
            ser = PhotoSerializer(photo)
            return Response(ser.data)
        except:
            return Response({'xato': "bu id xato"})

    def delete(self, request, id):
        photo = Photo.objects.get(id=id)
        photo.delete()
        return Response({'deleted':'successfully'})


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
    parser_classes = [JSONParser, MultiPartParser]
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
        # try:
        bolim = Bolim.objects.get(id=id)
        ser = BolimSerializer(bolim)
        xodim = Xodim.objects.filter(bulimi=bolim)
        for x in xodim:
            h = Hisobot.objects.filter(xodim=x)
        l=[]
        for i in h:
            found = False
            for item in l:
                if item['bulim_name'] == i.xodim.bulimi.name:
                    item['xato_soni'] += i.xato_soni
                    item['butun_soni'] += i.butun_soni
                    found = True
                    break
            if not found:
                l.append({'bulim_name': i.xodim.bulimi.name, 'xato_soni': i.xato_soni, 'butun_soni': i.butun_soni})
        # for i in h:
        #     found2 = False
        #     for item in l:
        #         if item['xato_name'] == i.xato.name:
        #             item['xato_soni'] += i.xato_soni
        #             found2 = True
        #             break
        #     if not found2:
        #         l.append({'xato_name': i.xato.name, 'xato_soni': i.xato_soni})
        return Response({'data':ser.data,
                                # 'all_statistic': s,
                                # 'mahsulot_xato_soni':d,
                                'statistic':l,
                                })
        # except:
        #     return Response({'xato': "bu id xato"})

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
        photo = request.data.getlist('photo', [])
        serializer = HisobotSerializer(data=request.data)
        if serializer.is_valid():
            d = serializer.save()
            for x in photo:
                s = Photo.objects.create(photo=x)
                d.photo.add(s)
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
        a = request.data.getlist('photo', [])
        hisobot = Hisobot.objects.get(id=id)
        serializer = HisobotSerializer(hisobot, data = request.data, partial=True)
        if serializer.is_valid():
            s = serializer.save()
            if a:
                for x in a:
                    n = Photo.objects.create(photo=x)
                    s.photo.add(n)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        hisobot = Hisobot.objects.get(id=id)
        hisobot.delete()
        return Response(status=204)

        


