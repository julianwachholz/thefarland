from django import forms
from utils.forms import KwargsPopMixin, ManagerKwargsMixin
from .models import Order


class OrderForm(KwargsPopMixin, forms.Form):
    pop_kwargs = ('user', 'product')
    notes = forms.CharField(label='Notes', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.extra_fields = []
        for name, field in self.product.get_form_fields():
            self.extra_fields.append(name)
            self.fields[name] = field

    def save(self):
        fields = {
            name: self.cleaned_data[name] for name in self.extra_fields
        }
        return Order.objects.create(
            user=self.user,
            product=self.product,
            notes=self.cleaned_data['notes'],
            fields=fields
        )
