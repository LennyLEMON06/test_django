from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('/')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
