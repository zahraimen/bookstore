from django import forms
from .models import Comment


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'recommend']


class AnonymousCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'text', 'recommend']
