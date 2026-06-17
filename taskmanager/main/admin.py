from django.contrib import admin
from .models import UserProfile, SleepDiary, Statistics


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'birth_date']
    search_fields = ['user__username', 'city']


@admin.register(SleepDiary)
class SleepDiaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'sleep_quality', 'duration_hours']
    list_filter = ['user', 'sleep_quality']
    search_fields = ['user__username', 'notes']


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['sleep_record', 'temperature', 'pressure', 'humidity']
    search_fields = ['sleep_record__user__username']