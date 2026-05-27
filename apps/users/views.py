from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm


def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect('core:index')


class RegisterView(CreateView):
    """Регистрация нового пользователя"""
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматический вход после регистрации
        login(self.request, self.object)
        return response


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    orders = request.user.orders.all() if hasattr(request.user, 'orders') else []
    return render(request, 'users/profile.html', {'orders': orders})
