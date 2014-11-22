from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from vanilla import CreateView, UpdateView, FormView, TemplateView

from apps.minecraft.commands import send_verification_code
from utils.views import UserFormKwargsMixin, SuccessMessageMixin

from .forms import UserCreateForm, UserUpdateForm, PasswordChangeForm, VerifyMinecraftUsernameForm


User = get_user_model()


def logout(request):
    """
    Logs out the user and displays 'You are logged out' message.

    """
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


class UserCreateView(SuccessMessageMixin, CreateView):
    """
    Register a new user.

    """
    model = User
    form_class = UserCreateForm
    template_name_suffix = '_create'

    success_url = reverse_lazy('accounts:verify')
    success_message = 'Thank you for registering.'

    def form_valid(self, form):
        """
        Create the new user and log them in directly.

        """
        form.save()
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        login(self.request, user)
        return super(UserCreateView, self).form_valid(form)

user_create = UserCreateView.as_view()


class UserUpdateView(UserFormKwargsMixin, SuccessMessageMixin, UpdateView):
    """
    Update user details.

    """
    model = User
    form_class = UserUpdateForm

    success_url = reverse_lazy('accounts:user_update')
    success_message = 'Details updated.'

    def get_object(self):
        return self.request.user

user_update = login_required(UserUpdateView.as_view())


class PasswordChangeView(UserFormKwargsMixin, SuccessMessageMixin, FormView):
    """
    Users should be able to change their password.

    """
    form_class = PasswordChangeForm
    template_name = 'auth/password_form.html'

    success_url = reverse_lazy('accounts:user_update')
    success_message = 'Password changed.'

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)

password_change = login_required(PasswordChangeView.as_view())


class VerifyFormView(UserFormKwargsMixin, SuccessMessageMixin, FormView):
    """
    Verify the username via a Minecraft server.

    """
    form_class = VerifyMinecraftUsernameForm
    template_name = 'accounts/verify.html'

    success_url = reverse_lazy('index')
    success_message = 'Your username has been verified.'

    def form_valid(self, form):
        form.save()
        return super(VerifyFormView, self).form_valid(form)

verify = login_required(VerifyFormView.as_view())


@login_required
def get_verify_token(request):
    """
    Send verification token to minecraft user.

    """
    if request.method == 'POST':
        send_verification_code(
            username=request.user.username,
            code=request.user.verification_code
        )
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'FAIL'})
