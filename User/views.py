from django.shortcuts import render
from .models import *
from .serializers import *
from Statistika.views import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime, timedelta
from django.utils import timezone


class ChangePasswordView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            if not check_password(old_password, user.password):
                return Response({"detail": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            # If you are using TokenAuthentication, you may need to update the token here
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "detail": "Password updated successfully",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request):
        user = User.objects.all()
        ser = UserSerializer(user, many=True)
        return Response(ser.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            status_value = serializer.validated_data.get('status')
            if status_value in ['Direktor', 'Admin']:
                if User.objects.filter(status=status_value).exists():
                    return Response({'message': f'{status_value} oldin yaratilgan'})
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
            return Response({'message': "bu id xato"})

    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data = request.data, partial=True)
        if serializer.is_valid():
            status_value = serializer.validated_data.get('status')
            if status_value in ['Direktor', 'Admin']:
                if User.objects.exclude(id=id).filter(status=status_value).exists():
                    return Response({'message': f'{status_value} oldin yaratilgan'})
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response({'message':'user o\'chirildi'})


class XodimView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        now = timezone.now()
        
        one_year_ago = now - timedelta(days=365)
        six_months_ago = now - timedelta(days=30*6)
        three_months_ago = now - timedelta(days=30*3)
        one_month_ago = now - timedelta(days=30)
        one_week_ago = now - timedelta(days=7)
        one_day_ago = now - timedelta(days=1)

        statistics = []

        def calculate_statistics(start_date, end_date):
            xodims = Xodim.objects.all()
            data = []
            for xodim in xodims:
                hisobots = Hisobot.objects.filter(xodim=xodim, created_at__range=[start_date, end_date])
                total_ish_vaqti = 0
                total_xato_soni = 0
                total_butun_soni = 0
                total_mistakes = 0
                xato_foizi = 0
                butun_foizi = 0
                for hisobot in hisobots:
                    total_ish_vaqti += hisobot.ish_vaqti
                    total_xato_soni += hisobot.xato_soni
                    total_butun_soni += hisobot.butun_soni
                    total_mistakes = total_xato_soni + total_butun_soni
                    xato_foizi = round((total_xato_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                    butun_foizi = round((total_butun_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                    # print(xato_foizi)
                    # print(butun_foizi)
                data.append({
                    'ism': xodim.first_name,
                    'ish_vaqti': total_ish_vaqti,
                    'xato_soni': total_xato_soni,
                    'butun_soni': total_butun_soni,
                    'Xato_foizi': xato_foizi,
                    'Butun_foizi': butun_foizi,
                })
            return data

        statistics.append({'period': '1 year', 'data': calculate_statistics(one_year_ago, now)})
        statistics.append({'period': '6 months', 'data': calculate_statistics(six_months_ago, now)})
        statistics.append({'period': '3 months', 'data': calculate_statistics(three_months_ago, now)})
        statistics.append({'period': '1 month', 'data': calculate_statistics(one_month_ago, now)})
        statistics.append({'period': '1 week', 'data': calculate_statistics(one_week_ago, now)})
        statistics.append({'period': '1 day', 'data': calculate_statistics(one_day_ago, now)})

        xodim = Xodim.objects.all()
        ser = XodimSerializer(xodim, many=True)
        return Response({'data':ser.data, 'all_statistics':statistics})

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
            l=[]
            m=[]
            h = Hisobot.objects.filter(xodim=xodim)
            sum_xato = h.aggregate(soni=Sum('xato_soni'))['soni'] or 0
            sum_butun = h.aggregate(soni=Sum('butun_soni'))['soni'] or 0
            total_mistakes = sum_xato + sum_butun
            xato_foizi = round((sum_xato * 100) / (total_mistakes) if total_mistakes else 0, 2)
            butun_foizi = round((sum_butun * 100) / (total_mistakes) if total_mistakes else 0, 2)
            all_statistic = {
                'id': xodim.id,
                'xodimi': xodim.first_name,
                'Jami_xato': sum_xato,
                'Jami_butun': sum_butun,
                'Xato_foizi': xato_foizi,
                'Butun_foizi': butun_foizi
            }
            d={}
            for j in h:
                xodim_mistakes = Hisobot.objects.filter(xodim=j.xodim, mahsulot=j.mahsulot)
                xodim_mistakes_aggregated = xodim_mistakes.aggregate(total_xato_soni=Sum('xato_soni'))
                d[str(j.mahsulot.name)] = xodim_mistakes_aggregated['total_xato_soni']
            l = []
            for j in h:
                found = False
                for item in l:
                    if item['mahsulot_name'] == j.mahsulot.name:
                        item['xato_soni'] += j.xato_soni
                        item['butun_soni'] += j.butun_soni
                        found = True
                        break
                if not found:
                    l.append({'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni, 'Xato_foizi': None, 'Butun_foizi': None})
            for i in h:
                for item in l:
                    if item['mahsulot_name'] == i.mahsulot.name:
                        item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                        item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 
            return Response({'data':ser.data,
                                    'all_statistic': all_statistic,
                                    'mahsulot_xato_soni':d,
                                    'statistic':l,
                                    })
        except:
            return Response({'message': "bu id xato"})

    def patch(self, request, id):
        a = request.data.getlist('ish_turi', [])
        xodim = Xodim.objects.get(id=id)
        ser = XodimSerializer(xodim, data = request.data, partial=True)
        if ser.is_valid():
            s = ser.save()
            if a:
                s.ish_turi.clear()
                for x in a:
                    s.ish_turi.add(x)
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, id):
        xodim = Xodim.objects.get(id=id)
        xodim.delete()
        return Response({'message':'xodim o\'chirildi'})

    