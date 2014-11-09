from django import forms
from django.contrib.auth import get_user_model


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


class UserUpdateForm(UserForm):
    """
    Update user details.

    """
    class Meta:
        model = User
        fields = UserForm.Meta.fields + (
            'username',
        )


class PasswordChangeForm(forms.Form):
    """
    Let a user change their password.

    """
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New password')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

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


class VerifyMinecraftUsernameForm(forms.Form):
    """
    Verify the username via a Minecraft server.

    """
    verification_code = forms.CharField(label='Verification Code')
