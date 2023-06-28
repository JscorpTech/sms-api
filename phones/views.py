from uuid import uuid4

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from helpers.ucell import Ucell
from phones.models import Phones


class SendSmsPage(View):

    def get(self, request):
        return render(request, "phone/create.html")

    def post(self, request: HttpRequest):
        data = request.POST

        phone = str(data.get("phone")).replace("+", "").replace(" ", "").replace("-", "").replace(")", "").replace("(",
                                                                                                                   "")
        check = Phones.objects.filter(user=request.user, phone=phone)
        if check.exists():
            messages.error(request, "Telefon nomer mavjud", extra_tags="danger")

        elif not phone.isdigit() or len(phone) != 12:
            messages.error(request, "Telefon nomer xato kiritildi", extra_tags="danger")

        elif f"{phone[3]}{phone[4]}" != "94" and f"{phone[3]}{phone[4]}" != "93":
            messages.error(request, "Iltimos Ucell nomerdan foydalaning", extra_tags="danger")
        else:
            user = Ucell(phone)
            response = user.sendOtp()
            request.session['phone'] = phone
            return redirect(reverse("phone:verify"))
        return render(request, "phone/create.html")


class VerifyPage(View):

    def get(self, request: HttpRequest):
        phone = request.session.get("phone", None)

        if phone is None:
            return redirect(reverse("phone:send-sms"))
        return render(request, "phone/verify.html")

    def post(self, request: HttpRequest):
        otp = request.POST.get("otp", None)
        phone = request.session.get("phone", None)

        if phone is None:
            return redirect(reverse("phone:send-sms"))

        if otp is None:
            messages.error(request, "Tasdiqlash ko'dini kiritmadingiz", extra_tags="danger")
            return render(request, "phone/verify.html")

        otp = str(otp).replace("-", "")
        if not otp.isdigit():
            messages.error(request, "Tasdiqlash ko'di nato'g'ri kiritildi", extra_tags="danger")
        elif len(str(otp)) != 6:
            messages.error(request, "Tasdiqlash ko'di to'liq emas", extra_tags="danger")
        else:
            user = Ucell(phone)
            response = user.setPassword(otp=otp)
            if response['success'] == True or response[
                'msg'] == "Новый пароль не отличается от текущего. Пожалуйста, выберите другой пароль.":
                messages.success(request, "Telefon nomer qo'shildi")
                Phones.objects.create(phone=phone, user=request.user, token=uuid4())
                return redirect(reverse("phone:list"))
            else:
                messages.error(request, response['msg'], extra_tags="danger")

        return render(request, "phone/verify.html")


class ListPage(ListView):
    template_name = "phone/list.html"
    model = Phones
    context_object_name = "phones"

    def get_queryset(self):
        return Phones.objects.filter(user=self.request.user)
