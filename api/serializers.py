from rest_framework import serializers


class SendSmsSerializer(serializers.Serializer):
    sms = serializers.CharField(max_length=255, error_messages={"blank": "Xabarni kiritmadingiz"})
    phone = serializers.IntegerField(error_messages={"blank": "Telefon nomer mavjud emas"})
    token = serializers.CharField(max_length=255, error_messages={
        "blank": "Token mavjud emas token olish uchun https://sms.iprogrammer.uz saytida ro'yhatdan o'ting"})
