from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    city = models.CharField('Город', max_length=100)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.city}"


class SleepDiary(models.Model):
    QUALITY_CHOICES = [
        (1, '⭐ Ужасно'),
        (2, '⭐⭐ Плохо'),
        (3, '⭐⭐⭐ Нормально'),
        (4, '⭐⭐⭐⭐ Хорошо'),
        (5, '⭐⭐⭐⭐⭐ Отлично'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_records')
    date = models.DateField('Дата сна')
    bedtime = models.DateTimeField('Время засыпания')
    wake_time = models.DateTimeField('Время пробуждения')
    sleep_quality = models.IntegerField('Качество сна', choices=QUALITY_CHOICES)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def duration_hours(self):
        if self.bedtime and self.wake_time:
            delta = self.wake_time - self.bedtime
            return round(delta.total_seconds() / 3600, 1)
        return None


class Statistics(models.Model):
    sleep_record = models.OneToOneField(
        SleepDiary,
        on_delete=models.CASCADE,
        related_name='weather'
    )
    pressure = models.FloatField('Давление (мм рт. ст.)')
    humidity = models.FloatField('Влажность (%)')
    temperature = models.FloatField('Температура (°C)')
    moon_phase = models.CharField('Фаза Луны', max_length=50)
    weather_condition = models.CharField('Погодные условия', max_length=100, blank=True)
    fetched_at = models.DateTimeField('Время получения', auto_now_add=True)

    def __str__(self):
        return f"{self.sleep_record.date} - {self.temperature}°C"