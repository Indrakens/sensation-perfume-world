from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.contrib import messages
from django.conf import settings 

from .forms import OrderForm 
from .models import Order, OrderLineItem  
from products.models import Product 
from bag.contexts import bag_contents 

import stripe 

def order_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        shopping_bag = request.session.get('bag', {}) 

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in shopping_bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                gift_bag_size=size,
                            ) 
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_shopping_bag')) 

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('order_checkout_success', args=[order.order_number])) 
        else:
            messages.error(request, 'There was an error with your form. \
                Please check your information.') 
                              
    else:    
        shopping_bag = request.session.get('bag', {}) 
        if not shopping_bag:
            messages.error(request, "Your shopping bag is empty.") 
            return redirect(reverse('products'))

        current_shopping_bag = bag_contents(request) 
        total = current_shopping_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY, 
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
             Did you forget to set it in your environment?')

    template = 'checkout/order_checkout.html'  
    context = {
        'order_form': order_form, 
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret, 
    } 

    return render(request, template, context) 


def order_checkout_success(request, order_number): 
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info') 
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.') 

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/order_checkout_success.html'
    context = {
        'order': order,
    } 

    return render(request, template, context)        
