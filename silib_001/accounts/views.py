from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as logedin, logout
from django.contrib.auth.decorators import login_required
# from .forms import SignupForm

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