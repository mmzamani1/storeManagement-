from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Market, Salesman, Product, Customer, Order, OrderItem
from .forms import MarketForm, SalesmanForm, ProductForm, CustomerForm, OrderForm, OrderItemForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django import forms


def home(request):
    return render(request, 'base.html')

# Generic views for Market
class MarketListView(LoginRequiredMixin, ListView):
    model = Market
    template_name = 'market/market_list.html'
    context_object_name = 'markets'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Market.objects.filter(market_name__icontains=query)
        return Market.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['additional_objects'] = Salesman.objects.all()
        context['additional_objects2'] = Customer.objects.all()
        
        return context

class MarketCreateView(LoginRequiredMixin, CreateView):
    model = Market
    form_class = MarketForm
    template_name = 'market/market_form.html'
    success_url = reverse_lazy('market_list')

class MarketUpdateView(LoginRequiredMixin, UpdateView):
    model = Market
    form_class = MarketForm
    template_name = 'market/market_form.html'
    success_url = reverse_lazy('market_list')

class MarketDeleteView(LoginRequiredMixin, DeleteView):
    model = Market
    template_name = 'market/market_confirm_delete.html'
    success_url = reverse_lazy('market_list')

# Salesman Views
class SalesmanListView(LoginRequiredMixin, ListView):
    model = Salesman
    template_name = 'salesman/salesman_list.html'
    context_object_name = 'salesmen'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Salesman.objects.filter(salesman_name__icontains=query)
        return Salesman.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        
        context['additional_objects'] = Product.objects.all()
        context['additional_objects2'] = Order.objects.all()
        
        return context

class SalesmanCreateView(LoginRequiredMixin, CreateView):
    model = Salesman
    form_class = SalesmanForm
    template_name = 'salesman/salesman_form.html'
    success_url = reverse_lazy('market_list')
    
    def form_valid(self, form):
        # Associate the OrderItem with the specific Order
        marketId = self.kwargs['pk']
        form.instance.market_id = marketId
        
        return super().form_valid(form)

class SalesmanUpdateView(LoginRequiredMixin, UpdateView):
    model = Salesman
    form_class = SalesmanForm
    template_name = 'salesman/salesman_form.html'
    success_url = reverse_lazy('market_list')

class SalesmanDeleteView(LoginRequiredMixin, DeleteView):
    model = Salesman
    template_name = 'salesman/salesman_confirm_delete.html'
    success_url = reverse_lazy('market_list')

# Product Views
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(product_name__icontains=query)
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        
        context['additional_objects'] = OrderItem.objects.all()
        
        return context 
    
    def setup(self, request, *args, **kwargs):
        
        products = Product.objects.all()
        
        for product in products:
            orderitems = OrderItem.objects.filter(product=product)
            
            for orderitem in orderitems:
                if orderitem.stock_state == False:
                    product.stock = product.stock - orderitem.quantity
                    orderitem.stock_state = True
                    orderitem.save()
                    
            product.save()
        
        return super().setup(request, *args, **kwargs)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('salesman_list')
    
    def form_valid(self, form):
        salesmanId = self.kwargs['pk']
        related_salesman = Salesman.objects.get(pk=salesmanId)
        related_market = related_salesman.market
        
        form.instance.salesman_id = salesmanId
        form.instance.market = related_market
        
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# Customer Views
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Customer.objects.filter(customer_name__icontains=query)
        return Customer.objects.all()

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')
    
    def form_valid(self, form):
        marketId = self.kwargs['pk']
        
        form.instance.market_id = marketId
        
        return super().form_valid(form)
    

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

# Order Views
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Order.objects.filter(customer__customer_name__icontains=query)
        return Order.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        orders = Order.objects.all()
        
        for order in orders:
            orderitems = OrderItem.objects.filter(order=order)
            
            for orderitem in orderitems:
                p = Product.objects.get(pk=orderitem.product.pk)   
                order.total_value += (p.price * orderitem.quantity)
                order.save()
        
        context['additional_objects'] = OrderItem.objects.all()
        
        return context
    
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')
    
    def form_valid(self, form):
        salesmanId = self.kwargs['pk']
        
        related_salesman = Salesman.objects.get(pk=salesmanId)
        related_market = related_salesman.market
        
        form.instance.salesman = related_salesman
        form.instance.market = related_market
        
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        salesmanId = self.kwargs['pk']
        related_salesman = Salesman.objects.get(pk=salesmanId)
        related_market = related_salesman.market
        
        form.fields['customer'].queryset = Customer.objects.filter(market=related_market)
        
        return form
    
class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')

def form_valid(self, form):
    salesmanId = self.kwargs['pk']
    
    related_salesman = Salesman.objects.get(pk=salesmanId)
    related_market = related_salesman.market
    
    form.instance.salesman = related_salesman
    form.instance.market = related_market
    
    return super().form_valid(form)
    
def get_form(self, form_class=None):
    form = super().get_form(form_class)
    
    salesmanId = self.kwargs['pk']
    related_salesman = Salesman.objects.get(pk=salesmanId)
    related_market = related_salesman.market
    
    form.fields['customer'].queryset = Customer.objects.filter(market=related_market)
    
    return form

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

# OrderItem Views
class OrderItemListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = 'orderitem/orderitem_list.html'
    context_object_name = 'orderitems'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return OrderItem.objects.filter(order__customer__customer_name__icontains=query)
        return OrderItem.objects.all()

class OrderItemCreateView(LoginRequiredMixin, CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'orderitem/orderitem_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        # Associate the OrderItem with the specific Order
        productId = self.kwargs['pk']
        related_product = Product.objects.get(pk=productId)
        
        form.instance.product = related_product
        
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        product_id = self.kwargs['pk']
        related_product = Product.objects.get(pk=product_id)
        related_salesman = related_product.salesman
        related_market = related_product.market
        quantity = related_product.stock

        form.fields['order'].queryset = Order.objects.filter(salesman=related_salesman, market=related_market)
        form.fields['quantity'].widget.attrs['max'] = quantity  
        form.fields['quantity'].max_value = quantity            

        return form

class OrderItemUpdateView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'orderitem/orderitem_form.html'
    success_url = reverse_lazy('product_list')
    

class OrderItemDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    template_name = 'orderitem/orderitem_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    
    def setup(self, request, *args, **kwargs):
        
        products = Product.objects.all()
        
        for product in products:
            orderitems = OrderItem.objects.filter(product=product)
            
            for orderitem in orderitems:
                if orderitem.stock_state == True:
                    product.stock = product.stock + orderitem.quantity
                    orderitem.stock_state = False
                    orderitem.save()
            
            product.save()
        
        return super().setup(request, *args, **kwargs)
