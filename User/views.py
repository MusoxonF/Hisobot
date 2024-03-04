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
                    return Response({'xabar': f'{status_value} oldin yaratilgan'})
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
        serializer = UserSerializer(user, data = request.data, partial=True)
        if ser.is_valid():
            status_value = serializer.validated_data.get('status')
            if status_value in ['Direktor', 'Admin']:
                if User.objects.exclude(id=id).filter(status=status_value).exists():
                    return Response({'xabar': f'{status_value} oldin yaratilgan'})
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
            l=[]
            s=[]
            m=[]
            h = Hisobot.objects.filter(xodim=xodim)
            sum_xato = h.aggregate(soni=Sum('xato_soni'))
            sum_butun = h.aggregate(soni=Sum('butun_soni'))
            s.append({
                'id': xodim.id,
                'xodimi': xodim.first_name,
                'Jami_xato': sum_xato,
                'Jami_butun': sum_butun,
            })
            d={}
            for j in h:
                a = j.mahsulot.name
                xodim_mistakes = Hisobot.objects.filter(xodim=j.xodim, mahsulot=j.mahsulot)
                xodim_mistakes_aggregated = xodim_mistakes.aggregate(total_xato_soni=Sum('xato_soni'))
                d[str(j.mahsulot.name)] = xodim_mistakes_aggregated['total_xato_soni']
            l={}
            for j in h:
                r={}
                if j.mahsulot.name in l:
                    l[str(j.mahsulot.name)]['xato_soni'] += j.xato_soni
                    l[str(j.mahsulot.name)]['butun_soni'] += j.butun_soni
                else:
                    r['xato_soni'] =j.xato_soni
                    r['butun_soni'] =j.butun_soni
                    l[str(j.mahsulot.name)] = r
                print(l)
            return Response({'data':ser.data,
                                    'all_statistic': s,
                                    'mahsulot_xato_soni':d,
                                    'statistic':l,
                                    })
        except:
            return Response({'xato': "bu id xato"})

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

    