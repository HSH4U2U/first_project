from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
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
        user.last_name = self.cleaned_data['nickname']
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user