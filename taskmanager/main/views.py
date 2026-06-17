from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать в Sleeper!")

def register(request):
    return HttpResponse("Страница регистрации")

def diary(request):
    return HttpResponse("Дневник сна")

def add_record(request):
    return HttpResponse("Добавление записи")

def edit_record(request, pk):
    return HttpResponse(f"Редактирование записи {pk}")

def delete_record(request, pk):
    return HttpResponse(f"Удаление записи {pk}")

def analytics(request):
    return HttpResponse("Аналитика сна")


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/'