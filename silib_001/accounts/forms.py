from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


def validate_school_email(value):
    if not "@uos.ac.kr" in value:
        raise ValidationError("서울시립대학교 이메일 형식만 아이디로 사용가능합니다.")
    else:
        return value

class SignupForm(UserCreationForm):
    username = forms.EmailField(validators=[validate_school_email])
    nickname = forms.CharField(max_length=8, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['username']
        user.last_name = self.cleaned_data['nickname']
        if commit:
            user.save()
        return user