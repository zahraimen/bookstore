from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreation(UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = UserCreationForm.Meta.fields + ('age',)
        fields = ('username', 'email', 'age',)


class CustomUserChange(UserChangeForm):
    class Meta:
        model = CustomUser
        # fields = UserChangeForm.Meta.fields
        fields = ('username', 'email', 'age',)
