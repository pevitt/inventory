from django.shortcuts import render
from rest_framework import permissions
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_apps.authentication.permissions import IsAdminUser, IsPurchaseUser, IsSalesUser
from utils.exceptions import InventoryAPIException, ErrorCode
from rest_framework import status
from django_apps.products import services as products_services
from django_apps.products import selectors as products_selectors


# Create your views here.
class PurchaseOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsPurchaseUser]

    class InputPurchaseOrderSerializer(serializers.Serializer):
        product_id = serializers.UUIDField(
            required=True
        )
        quantity = serializers.IntegerField(
            required=True
        )
        unit_cost = serializers.FloatField(
            required=True
        )
        total_cost = serializers.FloatField(
            required=False,
            default=0
        )

        def validate(self, attrs):
            if attrs['quantity'] <= 0:
                raise InventoryAPIException(ErrorCode.OP1)

            if attrs['unit_cost'] <= 0:
                raise InventoryAPIException(ErrorCode.OP3)

            product = products_selectors.get_product_by_id(
                id=attrs['product_id']
            )
            if not product.exists():
                raise InventoryAPIException(ErrorCode.P01)

            attrs['total_cost'] = attrs['unit_cost'] * attrs['quantity']

            return attrs

    class OutputPurchaseOrderSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        product_name = serializers.CharField()
        quantity = serializers.IntegerField()
        unit_cost = serializers.FloatField()
        total_cost = serializers.FloatField()
        purchase_date = serializers.DateTimeField()
        status = serializers.CharField()

    def post(self, request):
        in_serializer = self.InputPurchaseOrderSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = products_services.create_purchase_order(
            **in_serializer.validated_data
        )
        try:
            out_serializer = self.OutputPurchaseOrderSerializer(data=data)
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.OP0)

        return Response(
            data=out_serializer.validated_data,
            status=status.HTTP_201_CREATED
        )


class SaleOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsSalesUser | IsPurchaseUser]

    class InputSaleOrderSerializer(serializers.Serializer):
        product_id = serializers.UUIDField(
            required=True
        )
        quantity = serializers.IntegerField(
            required=True
        )
        unit_price = serializers.FloatField(
            required=False,
            default=0
        )
        total_price = serializers.FloatField(
            required=False,
            default=0
        )

        def validate(self, attrs):
            if attrs['quantity'] <= 0:
                raise InventoryAPIException(ErrorCode.S01)

            product = products_selectors.get_product_by_id(
                id=attrs['product_id']
            )
            if not product.exists():
                raise InventoryAPIException(ErrorCode.P01)

            if product.first().stock < attrs['quantity']:
                raise InventoryAPIException(ErrorCode.S02)

            attrs['unit_price'] = product.first().price

            attrs['total_price'] = attrs['unit_price'] * attrs['quantity']

            return attrs

    class OutputSaleOrderSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        product_name = serializers.CharField()
        quantity = serializers.IntegerField()
        unit_price = serializers.FloatField()
        total_price = serializers.FloatField()
        sale_date = serializers.DateTimeField()
        status = serializers.CharField()

    def post(self, request):
        in_serializer = self.InputSaleOrderSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = products_services.create_sale_order(
            **in_serializer.validated_data
        )
        try:
            out_serializer = self.OutputSaleOrderSerializer(data=data)
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.OS0)

        return Response(
            data=out_serializer.validated_data,
            status=status.HTTP_201_CREATED
        )