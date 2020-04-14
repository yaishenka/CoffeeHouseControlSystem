from django.db import models
from django.contrib.auth import get_user_model
import uuid

class AbstractProduct(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField(blank=False)

    @property
    def total_price(self):
        return self.price


class OrderPiece(models.Model):
    product = models.ForeignKey(AbstractProduct, on_delete=models.CASCADE)
    count = models.IntegerField(blank=False)

    @property
    def total_price(self):
        return self.product.price


class Purchase(models.Model):
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_positions = models.ManyToManyField(OrderPiece)
    time = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(blank=False, unique=True, default=uuid.uuid4, editable=False)

    @property
    def total_price(self):
        total_price = 0.0
        for order_position in self.order_positions.all():
            total_price += order_position.total_price

        return total_price
