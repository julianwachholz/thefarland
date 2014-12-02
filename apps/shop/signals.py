from .models import Order


def payment_received(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == 'Completed':
        order_id = ipn_obj.invoice.split('-')[1]
        Order.objects.filter(id=order_id).update(status=Order.PAID)
