from django.urls import include, path
from .views import PurchaseOrderView, SaleOrderView

urlpatterns = [
    path(
        'purchase/',
        PurchaseOrderView.as_view(),
        name='purchase'
    ),
    path(
        'sale/',
        SaleOrderView.as_view(),
        name='sale'
    )
]