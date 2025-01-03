from django.contrib import admin
from .models import Market, Salesman, Product, Customer, Order, OrderItem

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('market_id', 'market_name', 'location')
    search_fields = ('market_name', 'location')
    list_filter = ('location',)

@admin.register(Salesman)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = ('salesman_id', 'salesman_name', 'market')
    search_fields = ('salesman_name',)
    list_filter = ('market',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'price', 'stock', 'market', 'salesman')
    search_fields = ('product_name',)
    list_filter = ('market', 'salesman', 'price')
    list_editable = ('price', 'stock')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'email', 'market')
    search_fields = ('customer_name', 'email')
    list_filter = ('market',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'order_date', 'market', 'salesman')
    search_fields = ('customer__customer_name',)
    list_filter = ('order_date', 'market', 'salesman')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order', 'product', 'quantity', 'stock_state')
    search_fields = ('order__order_id', 'product__product_name')
    list_filter = ('product',)
    list_editable = ('stock_state',)