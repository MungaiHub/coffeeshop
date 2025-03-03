from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import coffee, Order


def home(request):
    Coffee = coffee.objects.all()
    return render(request, 'home.html',{'Coffee':Coffee})

def add_to_cart(request, coffee_id):
    # Get the coffee item
    Coffee = get_object_or_404(coffee, id=coffee_id)
    
    # Initialize the cart in the session if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    # Add the coffee ID to the cart or increment its quantity
    cart = request.session['cart']
    if str(coffee_id) in cart:
        cart[str(coffee_id)] += 1
    else:
        cart[str(coffee_id)] = 1
    
    request.session.modified = True  # Save the session
    
    # Optional: Add a success message
    messages.success(request, f"{Coffee.name} added to cart!")
    
    # Redirect back to the home page
    return redirect('home')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for coffee_id, quantity in cart.items():
        item = coffee.objects.get(id=int(coffee_id))
        item.quantity = quantity  # Add quantity to the item object
        item.subtotal = item.price * quantity  # Calculate subtotal
        total_price += item.subtotal  # Add to total price
        cart_items.append(item)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_status.html', {'order': order})

def checkout(request):
    if request.method == 'POST':
        # Get customer details from the form
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email')

        # Get the cart from the session
        cart = request.session.get('cart', {})

        # Calculate the total price
        total_price = 0
        for coffee_id, quantity in cart.items():
            item = coffee.objects.get(id=int(coffee_id))
            total_price += item.price * quantity

        # Create a new order
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            items=cart,
            total_price=total_price,
            status='pending'
        )

        # Clear the cart after placing the order
        request.session['cart'] = {}
        request.session.modified = True

        # Add a success message
        messages.success(request, f"Order #{order.id} placed successfully!")

        # Redirect to the home page or order confirmation page
        return redirect('home')

    return render(request, 'checkout.html')
