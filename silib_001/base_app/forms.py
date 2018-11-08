from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['restaurant', 'taste_star', 'price_star', 'clean_star', 'dish_eaten', 'content', 'food_image', ]
