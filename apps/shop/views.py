from vanilla import ListView, CreateView, DetailView
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse
from utils.views import UserFormKwargsMixin
from .models import Product, Order
from .forms import OrderForm


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

product_list = ProductListView.as_view()


class ProductOrderView(UserFormKwargsMixin, CreateView):
    model = Order
    form_class = OrderForm

    @cached_property
    def product(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product': self.product,
        })
        return super(ProductOrderView, self).get_context_data(**kwargs)

    def get_form(self, *args, **kwargs):
        kwargs.update({'product': self.product})
        return super(ProductOrderView, self).get_form(*args, **kwargs)

product_order = login_required(ProductOrderView.as_view())


class OrderMixin(object):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderListView(OrderMixin, ListView):
    context_object_name = 'orders'

order_list = login_required(OrderListView.as_view())


class OrderDetailView(OrderMixin, DetailView):

    def post(self, *args, **kwargs):
        return super(OrderDetailView, self).get(*args, **kwargs)

    def get_notify_host(self):
        if settings.DEBUG:
            return 'https://thefarland.ngrok.com'
        return 'https://thefar.land'

    def get_context_data(self, **kwargs):
        from_paypal = self.request.GET.get('from_paypal', False)
        if from_paypal:
            kwargs.update({
                'check_ipn': True,
            })
        elif self.object.needs_payment():
            from paypal.standard.forms import PayPalPaymentsForm
            form = PayPalPaymentsForm(initial={
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": self.object.product.amount,
                "currency_code": self.object.product.currency,
                "item_name": self.object.product.name,
                "invoice": 'THEFARLAND-' + str(self.object.pk),
                "notify_url": self.get_notify_host() + reverse('paypal-ipn'),
                "return_url": (self.get_notify_host() +
                               reverse('shop:order_detail', kwargs={'pk': self.object.pk}) +
                               '?from_paypal=true'),
                "cancel_return": self.get_notify_host() + reverse('shop:order_detail', kwargs={'pk': self.object.pk}),
            })
            kwargs.update({
                'form': form,
            })
        return super(OrderDetailView, self).get_context_data(**kwargs)

order_detail = login_required(csrf_exempt(OrderDetailView.as_view()))


@login_required
def order_redeem(request, pk):
    qs = Order.objects.filter(user=request.user)
    order = get_object_or_404(qs, pk=pk)

    if not order.can_redeem():
        return JsonResponse({
            'status': 'FAIL',
            'error': 'Cannot redeem this order.',
        })

    from apps.minecraft.tasks import minecraft_cmd
    command = order.product.delivery_command.format(user=order.user.username)
    minecraft_cmd.delay(command)

    order.redeemed = True
    order.save()

    return JsonResponse({
        'status': 'OK',
    })
