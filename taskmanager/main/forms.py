from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import SleepDiary, UserProfile


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, label='Email')
    city = forms.CharField(max_length=100, required=True, label='Город')
    birth_date = forms.DateField(
        required=False,
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'city', 'birth_date', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Это поле обязательно.')
        if len(username) < 3:
            raise ValidationError('Имя пользователя должно содержать минимум 3 символа.')
        if len(username) > 150:
            raise ValidationError('Имя пользователя не должно превышать 150 символов.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                city=self.cleaned_data['city'],
                birth_date=self.cleaned_data.get('birth_date')
            )
        return user


class SleepDiaryForm(forms.ModelForm):
    """Форма для добавления записи о сне"""

    class Meta:
        model = SleepDiary
        fields = ['date', 'bedtime', 'wake_time', 'sleep_quality', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bedtime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'wake_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'sleep_quality': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'