from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('add_to_cart/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('cart/', views.view_cart, name='view_cart'),  # View cart
    path('checkout/', views.checkout, name='checkout'),
    path('order_status/<int:order_id>/', views.order_status, name='order_status'),  # Checkout page
]

