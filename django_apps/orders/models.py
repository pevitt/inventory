from datetime import datetime

from django.db import models
from django_apps.products.models import Products
from utils.models import BaseModel


# Create your models here.
class PurchaseOrder(BaseModel):
    PURCHARSE_ORDER_STATUS = (
        ('RECEIVED', 'RECEIVED'),
        ('CANCELLED', 'CANCELLED'),
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='purchase_order_product'
    )
    quantity = models.IntegerField()
    unit_cost = models.FloatField()
    total_cost = models.FloatField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=PURCHARSE_ORDER_STATUS,
        default='RECEIVED'
    )

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'purchase_order'
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']


class SaleOrder(BaseModel):
    SALE_ORDER_STATUS = (
        ('ACCEPTED', 'ACCEPTED'),
        ('CANCELLED', 'CANCELLED'),
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='sale_order_product'
    )
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    sale_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=SALE_ORDER_STATUS,
        default='ACCEPTED'
    )

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'sale_order'
        verbose_name = 'Sale Order'
        verbose_name_plural = 'Sale Orders'
        ordering = ['-created_at']
