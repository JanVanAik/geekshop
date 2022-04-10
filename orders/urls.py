from django.urls import path

from orders.views import order_forming_complete, OrderListView, \
    OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView

app_name = 'orders'

urlpatterns =[
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete')
]
