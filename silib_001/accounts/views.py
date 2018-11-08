from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as logedin, logout, authenticate
from .forms import SignupForm
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage



def login(request):
    form = AuthenticationForm(data=request.POST)
    alert_message = ""
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            logedin(request, user)
            # return redirect(request.path)
            return redirect('base_app:base')
        else:
            form = AuthenticationForm()
            alert_message = "아이디나 비밀번호를 바르게 입력해주세요."
    ctx = {
        'form': form,
        'alert_message': alert_message,
    }
    return render(request, 'accounts/login.html', ctx)


def view_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('base_app:base')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # form.alert = "회원가입에 성공하셨습니다. 더 많은 서비스 이용을 위해 로그인 해주세요."
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('accounts/user_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '<a href="https://portal.uos.ac.kr/user/login.face">'
                '학교 이메일</a><span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )
    else:
        form = SignupForm()
        ctx = {'form': form}
        return render(request, 'accounts/signup.html', ctx)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        logedin(request, user)
        return redirect('base_app:base')
    else:
        return HttpResponse('비정상적인 접근입니다.')