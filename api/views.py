from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import SendSmsSerializer
from helpers.ucell import Ucell
from phones.models import Phones


class SendSmsApi(APIView):
    serializer_class = SendSmsSerializer

    def post(self, request):
        ser = SendSmsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)

        sms = ser.data.get("sms")
        token = ser.data.get("token")

        phone = Phones.objects.filter(token=token)
        if not phone.exists():
            return Response({'success': False,
                             "msg": "Token xato!!! token olish uchun https://sms.iprogrammer.uz saytida ro'yhatdan o'ting"})
        user = Ucell(phone.first().phone)
        res = user.sendMessage(ser.data.get("phone"), sms)

        return Response(res)
