from django.db import models
from utils.models import BaseModelUUID, BaseModel
from decimal import Decimal


# Create your models here.
class Departments(BaseModel):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    code = models.CharField(
        max_length=5,
        unique=True
    )
    margin_percentage = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name}'


class Products(BaseModelUUID):
    department = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    code = models.CharField(
        max_length=10,
        unique=True
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.IntegerField(
        null=True,
        blank=True,
        default=0
    )

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(
                fields=['name'],
                name='name_idx'
            )
        ]

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.pk:
            # Its no necessary to use de if else, because pk always exists in the object when is created
            # only created_at came empty, but a let it for the example
            try:
                product = Products.objects.get(id=self.pk)
                if product.cost != self.cost:
                    self.price = Decimal(self.cost) * Decimal(1 + (self.department.margin_percentage/100))
            except Products.DoesNotExist:
                self.price = Decimal(self.cost) * Decimal(1 + (self.department.margin_percentage/100))
                pass
        else:
            self.price = Decimal(self.cost) * Decimal(1 + (self.department.margin_percentage/100))

        super().save(*args, **kwargs)
