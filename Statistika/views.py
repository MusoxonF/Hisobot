from Mistakes.models import *
from User.models import *

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser

from django.db.models import Sum, Max, Min, Count, F, Q, Avg


class XodimStatistic(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    
    def get(self, request):
        x = Xodim.objects.all()
        l=[]
        s=[]
        for i in x:
            d = {}
            d['ism']=i.first_name
            h = Hisobot.objects.filter(xodim=i)
            # h = Hisobot.objects.filter(xodim=i).filter(mahsulot=j.mahsulot)
            sum_xato = h.aggregate(Sum('xato_soni'))
            sum_butun = h.aggregate(Sum('butun_soni'))
            s.append(
                {
                    'xodimi': i.first_name,
                    'xato_soni': sum_xato['xato_soni__sum'],
                    'butun_soni': sum_butun['butun_soni__sum'],
                }
            )
            for j in h:
                l.append({
                    'data':{
                    'jami_xato_soni': s.xato_soni
                    'jami_butun_soni': s.butun_soni
                    'mahsulot_name': j.mahsulot.name,
                    'xodimi': i.first_name,
                    'xato_soni': j.xato_soni,
                    'butun_soni': j.butun_soni,
                
                }})
        return Response([l])
