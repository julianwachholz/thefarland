from django import forms
from utils.forms import KwargsPopMixin, ManagerKwargsMixin
from .models import Order


class OrderForm(KwargsPopMixin, ManagerKwargsMixin, forms.ModelForm):
    pop_kwargs = ('user', 'product')

    class Meta:
        model = Order
        fields = ['notes']
