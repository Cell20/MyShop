from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


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
            # delay method of task to execute it asynchronously, it'll be added to the queue & will be executed by a worker asap.
            order_created.delay(order.id)
            context = {'order': order}
            # Thank you page
            return render(request, 'orders/order/created.html', context)
    else:
        form = OrderCreateForm()
        # Only one page is sent either the above one or below one
    context = {'cart': cart, 'form': form}
    # order form page
    return render(request, 'orders/order/create.html', context)
