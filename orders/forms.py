from django import forms

from orders.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', )


class OrderItemsForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=True)

    class Meta:
        model = OrderItem
        fields = '__all__'