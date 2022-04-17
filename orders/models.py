from django.db import models, transaction
from django.conf import settings
from products.models import Product


class OrderQuerySet(models.QuerySet):

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
            else:
                self.product.quantity -= self.quantity
            self.product.save()
            super(OrderQuerySet, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.product.quantity += self.quantity
            self.product.save()
            super(OrderQuerySet, self).delete(*args, **kwargs)


class Order(models.Model):
    FORMING = 1
    SENT_TO_PROCESS = 2
    PAID = 3
    PROCEED = 4
    READY = 5
    CANCEL = 6

    ORDER_STATUSES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCESS, 'В обработке'),
        (PAID, 'Оплачено'),
        (PROCEED, 'Собирается'),
        (READY, 'Готов'),
        (CANCEL, 'Отменен')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    update = models.DateTimeField(verbose_name='Время изменения', auto_now=True)
    status = models.PositiveIntegerField(choices=ORDER_STATUSES, verbose_name='Статус', default=FORMING)
    is_active = models.BooleanField(verbose_name='Является активным', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    @property
    def get_total_cost(self):
        items = self.items.select_related()
        return sum(list(map(lambda x: x.cost, items)))

    @property
    def get_total_quantity(self):
        items = self.items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def delete(self, using=None, keep_parents=False):
        for item in self.items.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save


class OrderItem(models.Model):
    objects = OrderQuerySet.as_manager()
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    @property
    def cost(self):
        return self.product.price * self.quantity
