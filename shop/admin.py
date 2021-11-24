from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Message)