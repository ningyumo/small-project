from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import UserProfile


class RegisterForm(forms.Form):
    gender = (
        ("mail", "男"),
        ("femail", "女"),
    )
    nick_name = forms.CharField(
        label="昵称",
        label_suffix="",
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入昵称，长度小于10",
            }
        )
    )
    tel = forms.CharField(
        label="手机",
        label_suffix="",
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    sex = forms.ChoiceField(
        label="性别",
        label_suffix="",
        choices=gender,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )
    username = forms.CharField(
        label="用户名",
        label_suffix="",
        max_length=10,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入用户名，长度小于10",
            }
        )
    )
    email = forms.EmailField(
        label="邮箱",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        label="密码",
        label_suffix="",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码，长度应大于6",
            }
        )
    )
    password_again = forms.CharField(
        label="重复密码",
        label_suffix="",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请再次输入密码",
            }
        )
    )

    def clean_nick_name(self):
        nick_name = self.cleaned_data['nick_name'].strip()
        if UserProfile.objects.filter(nick_name=nick_name).exists():
            raise forms.ValidationError("昵称已存在")
        if len(nick_name) < 0:
            raise forms.ValidationError("请输入昵称")
        if len(nick_name) > 10:
            raise forms.ValidationError("昵称长度不能大于10")
        return nick_name

    def clean_tel(self):
        tel = self.cleaned_data['tel'].strip()
        if len(tel) != 11:
            raise forms.ValidationError("请输入正确的手机号")
        try:
            tel = int(tel)
        except ValueError:
            raise forms.ValidationError("请输入正确的手机号")
        return tel

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        print(self.cleaned_data)
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if len(password) < 6 or len(password_again) < 6:
            raise forms.ValidationError("密码长度不能小于6")
        if password != password_again:
            raise forms.ValidationError("两次密码不一致")
        return password_again


class LoginForm(forms.Form):
    account = forms.CharField(
        label='账号',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '请输入手机/邮箱/用户名',
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='密码',
        label_suffix='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '请输入密码',
                'class': 'form-control',
            }
        )
    )
    captcha = CaptchaField(
        label='验证码',
        label_suffix='',
    )

    def clean(self):
        account = self.cleaned_data['account']
        password = self.cleaned_data['password']
        if account.isdigit() and len(account) and UserProfile.objects.filter(tel=account).exists():
            user = UserProfile.objects.get(tel=account).user
        elif User.objects.filter(email=account).exists():
            user = User.objects.get(email=account)
        elif User.objects.filter(username=account).exists():
            user = User.objects.get(username=account)
        else:
            raise forms.ValidationError("账号错误，请重新输入")
        user = auth.authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError("账号或密码错误，请重新输入")
        self.cleaned_data['user'] = user
        return self.cleaned_data
