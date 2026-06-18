from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .models import SleepDiary
from .forms import UserRegisterForm, SleepDiaryForm

def home(request):
    """Главная страница"""
    return render(request, 'main/home.html')

def register(request):
    """Регистрация"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('main:home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def diary(request):
    return HttpResponse("Дневник сна")

@login_required
def add_record(request):
    """Добавление записи о сне"""
    if request.method == 'POST':
        form = SleepDiaryForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Запись о сне добавлена!')
            return redirect('main:diary')
    else:
        form = SleepDiaryForm()
    return render(request, 'main/add_record.html', {'form': form})

def edit_record(request, pk):
    return HttpResponse(f"Редактирование записи {pk}")

def delete_record(request, pk):
    return HttpResponse(f"Удаление записи {pk}")

def analytics(request):
    return HttpResponse("Аналитика сна")


class CustomLoginView(LoginView):
    """Вход в систему"""
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/'