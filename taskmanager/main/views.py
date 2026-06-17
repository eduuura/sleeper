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
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/'


@login_required
def diary(request):
    """Дневник сна"""
    records = SleepDiary.objects.filter(user=request.user).select_related('weather')

    quality = request.GET.get('quality')
    if quality:
        records = records.filter(sleep_quality=quality)

    return render(request, 'main/diary.html', {'records': records})


@login_required
def add_record(request):
    """Добавление записи о сне"""
    if request.method == 'POST':
        form = SleepDiaryForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Запись добавлена!')
            return redirect('diary')
    else:
        form = SleepDiaryForm()
    return render(request, 'main/add_record.html', {'form': form})


@login_required
def edit_record(request, pk):
    """Редактирование записи"""
    record = get_object_or_404(SleepDiary, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SleepDiaryForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись обновлена!')
            return redirect('diary')
    else:
        form = SleepDiaryForm(instance=record)
    return render(request, 'main/add_record.html', {'form': form, 'record': record})


@login_required
def delete_record(request, pk):
    """Удаление записи"""
    record = get_object_or_404(SleepDiary, pk=pk, user=request.user)

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись удалена!')
        return redirect('diary')

    return render(request, 'main/delete_record.html', {'record': record})


@login_required
def analytics(request):
    """Страница аналитики"""
    records = SleepDiary.objects.filter(user=request.user).select_related('weather')
    return render(request, 'main/analytics.html', {'records': records})



