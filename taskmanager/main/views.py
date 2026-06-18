from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Avg, Count, Min, Max
from django.http import HttpResponse
from .models import SleepDiary
from .forms import UserRegisterForm, SleepDiaryForm
import pandas as pd


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


class CustomLoginView(LoginView):
    """Вход в систему"""
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

    sort = request.GET.get('sort', '-date')
    if sort in ['date', '-date', 'sleep_quality', '-sleep_quality']:
        records = records.order_by(sort)
    else:
        records = records.order_by('-date')

    return render(request, 'main/diary.html', {'records': records})


@login_required
def add_record(request):
    """Запись в дневник сна"""
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


@login_required
def edit_record(request, pk):
    """Редактирование записи"""
    record = get_object_or_404(SleepDiary, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SleepDiaryForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись обновлена')
            return redirect('main:diary')
    else:
        form = SleepDiaryForm(instance=record)

    return render(request, 'main/edit_record.html', {'form': form, 'record': record})


@login_required
def delete_record(request, pk):
    """Удаление записи"""
    record = get_object_or_404(SleepDiary, pk=pk, user=request.user)

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись удалена')
        return redirect('main:diary')

    return render(request, 'main/delete_record.html', {'record': record})


@login_required
def analytics(request):
    """Страница аналитики"""
    from django.db.models import Avg, Count, Min, Max
    from .models import SleepDiary
    import pandas as pd

    records = SleepDiary.objects.filter(user=request.user).select_related('weather')
    total_records = records.count()

    stats = {
        'total_records': total_records,
        'avg_quality': 0,
        'avg_duration': 0,
        'best_quality': 0,
        'worst_quality': 0,
        'avg_pressure': 0,
        'avg_temperature': 0,
        'avg_humidity': 0,
        'correlation': None,
    }

    if total_records > 0:
        stats['avg_quality'] = round(records.aggregate(Avg('sleep_quality'))['sleep_quality__avg'] or 0, 1)
        stats['best_quality'] = records.aggregate(Max('sleep_quality'))['sleep_quality__max'] or 0
        stats['worst_quality'] = records.aggregate(Min('sleep_quality'))['sleep_quality__min'] or 0

        #Срдлительность
        durations = [r.duration_hours for r in records if r.duration_hours]
        stats['avg_duration'] = round(sum(durations) / len(durations), 1) if durations else 0

        #Статистика
        weather_records = [r.weather for r in records if hasattr(r, 'weather')]
        if weather_records:
            stats['avg_pressure'] = round(sum(w.pressure for w in weather_records) / len(weather_records), 1)
            stats['avg_temperature'] = round(sum(w.temperature for w in weather_records) / len(weather_records), 1)
            stats['avg_humidity'] = round(sum(w.humidity for w in weather_records) / len(weather_records), 1)

            #Корреляция
            if len(weather_records) >= 3:
                df = pd.DataFrame([
                    {'pressure': w.pressure, 'quality': w.sleep_record.sleep_quality}
                    for w in weather_records
                ])
                corr = df['pressure'].corr(df['quality'])
                stats['correlation'] = round(corr, 2) if not pd.isna(corr) else None

    #Данные
    record_data = []
    for record in records.order_by('-date'):
        record_data.append({
            'date': record.date,
            'quality': record.get_sleep_quality_display(),
            'duration': record.duration_hours,
            'pressure': record.weather.pressure if hasattr(record, 'weather') else None,
            'temperature': record.weather.temperature if hasattr(record, 'weather') else None,
            'humidity': record.weather.humidity if hasattr(record, 'weather') else None,
            'moon_phase': record.weather.moon_phase if hasattr(record, 'weather') else None,
        })

    return render(request, 'main/analytics.html', {
        'stats': stats,
        'record_data': record_data,
        'total_records': total_records,
    })