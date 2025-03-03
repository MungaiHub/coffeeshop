from django.contrib import admin
from django.core.mail import send_mail
from .models import coffee, Order

class coffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        # Mark selected orders as completed
        queryset.update(status='completed')
        # Send confirmation emails
        for order in queryset:
            self.send_confirmation_email(order)
        self.message_user(request, f"{queryset.count()} orders marked as completed.")

    mark_as_completed.short_description = "Mark selected orders as completed"

    def send_confirmation_email(self, order):
        subject = f"Order #{order.id} Completed"
        message = f"Dear {order.customer_name},\n\nYour order has been completed. Thank you for shopping with us!"
        from_email = "amosmungai085@gmail.com"  # Replace with your email
        recipient_list = [order.customer_email]
        send_mail(subject, message, from_email, recipient_list)

    # Remove the "Add Order" button
    def has_add_permission(self, request):
        return False

admin.site.register(coffee, coffeeAdmin)
admin.site.register(Order, OrderAdmin)
