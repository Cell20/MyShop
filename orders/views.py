from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # delay method of task to execute it asynchronously, it'll be added to the queue & will be executed by a worker asa its idle.
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/order/created.html', locals())  # Thank you page
    else:
        form = OrderCreateForm()
        # Only one page is sent either the above one or below one
    context = {'cart': cart, 'form': form}
    # order form page
    return render(request, 'orders/order/create.html', context)
