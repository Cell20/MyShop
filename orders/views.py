from django.shortcuts import get_object_or_404, render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from decimal import Decimal

# convert cart.get_discount into order.get_discount to avoid sessions issues


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
                order.code = cart.coupon.code
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

            # delay method of task to execute it asynchronously, it'll be added to the queue & will be executed by a worker asa its idle.
            order_created(order.id)
            cart.clear()
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


@staff_member_required
def admin_order_detail(request, order_id):
    """Get the Order w/ ID and render a template to display the Order"""
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'admin/orders/order/detail.html', context)


@staff_member_required
def admin_order_pdf(request, order_id):
    """Generate the pdf for the orders."""
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    html = render_to_string('orders/order/pdf.html', context)  # save the html
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
