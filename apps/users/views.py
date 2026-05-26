from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('core:index')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('core:index')
