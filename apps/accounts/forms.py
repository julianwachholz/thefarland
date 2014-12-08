from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.minecraft.commands import team_add_registered
from utils.forms import KwargsPopMixin
from .models import AUTH_VERIFIED_GROUP

User = get_user_model()



class UserForm(forms.ModelForm):
    """
    User form.

    """
    class Meta:
        model = User
        fields = (
            'username',
        )


class UserCreateForm(UserForm):
    """
    A form to register a new user.

    """
    password = forms.CharField(label='Password')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserUpdateForm(KwargsPopMixin, UserForm):
    """
    Update user details.

    """
    class Meta:
        model = User
        fields = (
            'username',
        )

    def save(self, commit=True):
        if self.cleaned_data['username'] != self.initial['username']:
            self.user.is_verified = False
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(KwargsPopMixin, forms.Form):
    """
    Let a user change their password.

    """
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New password')

    def clean_current_password(self):
        """
        Just return True instead of the actual password.

        """
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError('Wrong password.')
        return True

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
        return self.user


class VerifyMinecraftUsernameForm(KwargsPopMixin, forms.Form):
    """
    Verify the username via a Minecraft server.

    """
    verification_code = forms.CharField(label='Verification Code')

    def clean_verification_code(self):
        if self.user.verification_code != self.cleaned_data['verification_code']:
            raise forms.ValidationError('Verification code is invalid.')
        return self.cleaned_data['verification_code']

    def save(self):
        try:
            group = Group.objects.get(name=AUTH_VERIFIED_GROUP)
            group.user_set.add(self.user)
        except Group.DoesNotExist:
            pass

        team_add_registered(self.user.username)
        self.user.is_verified = True
        self.user.verification_code = ''
        self.user.save()
