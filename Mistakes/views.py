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
            return Response({'message': "bu id xato"})

    def delete(self, request, id):
        photo = Photo.objects.get(id=id)
        photo.delete()
        return Response({'message':'successfully deleted'})


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
            return Response({'message': "bu id xato"})

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
        bolim = Bolim.objects.all()
        for i in bolim.user:
            if serializer.is_valid():
                user_value = serializer.validated_data.get('user')
                if user_value == i:
                    return Response({'message': 'bu user ishlatilgan'})
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors)


class BolimDetail(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request, id):
        bulim = Bolim.objects.get(id=id)
        ser = BolimSerializer(bulim)
        a = {}
        if Hisobot.objects.filter(xodim__bulimi=bulim):
            missed = Hisobot.objects.filter(xodim__bulimi=bulim)
            sum_xato = missed.aggregate(soni=Sum('xato_soni'))
            sum_butun = missed.aggregate(soni=Sum('butun_soni'))
            a[str('bulim_name')]=str(bulim.name)
            a[str('bulim_id')]=str(bulim.bulim_id)
            a[str('bulim_boshliq')]=str(bulim.user.first_name)
            a[str('xato_soni')]=sum_xato
            a[str('butun_soni')]=sum_butun
            a[str('hisobot_soni')]=len(missed)
            b = missed.aggregate(Count('xodim'))
            a[str('xodim_soni')]=b

            c = []
            for j in missed:
                found = False
                for item in c:
                    if item['mahsulot_name'] == j.mahsulot.name:
                        item['mahsulot_id'] += j.mahsulot.mahsulot_id
                        item['xato_soni'] += j.xato_soni
                        item['butun_soni'] += j.butun_soni
                        found = True
                        break
                if not found:
                    c.append({'mahsulot_name': j.mahsulot.name, 'mahsulot_id': j.mahsulot.mahsulot_id, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni})

            d = []
            for j in missed:
                found = False
                for item in d:
                    if item['xato_name'] == j.xato.name:
                        item['xato_id'] = j.xato.xato_id
                        item['mahsulot_name'] = j.mahsulot.name
                        item['xato_soni'] += j.xato_soni
                        found = True
                        break
                if not found:
                    d.append({'xato_name': j.xato.name, 'xato_id': j.xato.xato_id, 'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni})

            return Response({'data':ser.data,
                         'statistic':a,
                         'mahsulot':c,
                         'xato': d

                         })
        return Response({'data':ser.data,
                         'statistic':None,
                         'mahsulot':None,
                         'xato': None
                         })
            
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
            return Response({'message': "bu id xato"})

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
            return Response({'message': "bu id xato"})

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
            return Response({'message': "bu id xato"})
    
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

        


