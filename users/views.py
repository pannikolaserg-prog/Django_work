from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Отправка приветственного письма
            try:
                send_mail(
                    subject='Добро пожаловать!',
                    message=f'Здравствуйте, {user.first_name}!\n\nВы успешно зарегистрировались на нашем сайте.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Регистрация прошла успешно! Проверьте почту.')
            except Exception as e:
                messages.warning(request, f'Регистрация прошла, но письмо не отправлено: {e}')

            # Автоматически логиним пользователя после регистрации
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Регистрация'})


def user_login(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}!')

            # Перенаправление на страницу, откуда пришли
            next_url = request.GET.get('next', 'users:profile')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверный email или пароль')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form, 'title': 'Вход'})


@login_required
def user_logout(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('users:login')


@login_required
def profile(request):
    """Профиль пользователя с возможностью редактирования"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form, 'title': 'Мой профиль'})
