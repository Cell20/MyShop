from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
import braintree

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')  # current order
    order = get_object_or_404(Order, id=order_id)  # get order or raise 404
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)  # get nonce
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost: 2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            order.paid = True  # mark the order as paid
            order.braintree_id = result.transaction.id  # store unique trans id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = gateway.client_token.generate()  # generate token

        context = {'order': order, 'client_token': client_token}
        return render(request, 'payment/process.html', context)


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
