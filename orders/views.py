from django.db import transaction
from django.shortcuts import  get_object_or_404
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from baskets.models import Basket
from orders.forms import OrderItemsForm, OrderForm
from orders.models import Order, OrderItem


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model = Order


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemsForm, extra=basket_items.count()
                )
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['price'] = basket_items[num].product.price
                    form.initial['quantity'] = basket_items[num].quantity
            else:
                formset = OrderFormSet()
        context.update(orderitems=formset)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']


        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost == 0:
                self.object.delete()

            return super(OrderCreateView, self).form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:order_list')


class OrderUpdateView(UpdateView):
    model = Order


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCESS
    order.save()
