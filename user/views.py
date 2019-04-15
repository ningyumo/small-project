from django.shortcuts import render, redirect
from django.urls import reverse
from .form import RegisterForm, LoginForm
from .models import UserProfile
from django.contrib import auth
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                sex = form.cleaned_data['sex']
                nick_name = form.cleaned_data['nick_name']
                tel = form.cleaned_data['tel']
                print(type(tel))
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(username=username, password=password, email=email)
                user_profile = UserProfile.objects.create(nick_name=nick_name, tel=tel, sex=sex, user=user)
                auth.login(request, user)
                return redirect(reverse('home'))
        else:
            form = RegisterForm()
        context = {"form": form}
        return render(request, "user/register.html", context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth.login(request, user)
            return redirect(reverse("home"))
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))





