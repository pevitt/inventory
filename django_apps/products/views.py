from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from utils.exceptions import InventoryAPIException, ErrorCode
from django_apps.products import selectors as products_selectors
from django_apps.products import services as products_services
from django_apps.authentication.permissions import IsAdminUser, IsPurchaseUser
from .tasks import prueba_task


# Create your views here.
class DepartmentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsPurchaseUser]

    class OutPutDeparmentSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        code = serializers.CharField()
        margin_percentage = serializers.FloatField()

    def get(self, request):
        data = products_services.get_all_departments()
        out_serializer = self.OutPutDeparmentSerializer(data=data, many=True)
        # prueba_task.delay()
        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.E00)

        return Response(
            out_serializer.data,
            status=status.HTTP_200_OK
        )


class DepartmentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsPurchaseUser]

    class OutPutDeparmentSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        code = serializers.CharField()
        margin_percentage = serializers.FloatField()

    def get(self, request, department_id):
        data = products_services.get_department_by_id(
            department_id=department_id
        )
        out_serializer = self.OutPutDeparmentSerializer(data=data.__dict__)

        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.E00)

        return Response(
            out_serializer.data,
            status=status.HTTP_200_OK
        )

    class InputDepartmentPutSerialzer(serializers.Serializer):
        margin_percentage = serializers.FloatField(
            required=True
        )

    def put(self, request, department_id):
        in_serializer = self.InputDepartmentPutSerialzer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = products_services.update_department(
            department_id=department_id,
            **in_serializer.validated_data
        )
        out_serializer = self.OutPutDeparmentSerializer(data=data)
        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.D00)

        return Response(
            out_serializer.data,
            status=status.HTTP_202_ACCEPTED
        )


class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsPurchaseUser]

    class InputProductSerializer(serializers.Serializer):
        department_id = serializers.IntegerField(
            required=True
        )
        name = serializers.CharField(
            required=True
        )
        description = serializers.CharField(
            required=False
        )
        code = serializers.CharField(
            required=True
        )
        cost = serializers.FloatField(
            required=True
        )
        price = serializers.FloatField(
            required=False,
            default=0
        )
        stock = serializers.IntegerField(
            required=False,
            default=0
        )

        def validate(self, attrs):
            department_id = attrs.get('department_id')
            department_qry = products_selectors.get_department_by_id(id=department_id)
            if not department_qry.exists():
                raise InventoryAPIException(ErrorCode.D01)
            deparment = department_qry.first()

            # Create Code
            code_product = f"{deparment.code}-{attrs.get('code')}"
            attrs['code'] = code_product

            return attrs

    class OutputProductSerializer(serializers.Serializer):
        department = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField()
        code = serializers.CharField()
        cost = serializers.FloatField()
        price = serializers.FloatField()
        stock = serializers.IntegerField()

    def post(self, request):
        in_serializer = self.InputProductSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = products_services.create_product(
            **in_serializer.validated_data
        )
        out_serializer = self.OutputProductSerializer(data=data)

        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.P00)

        return Response(
            out_serializer.data,
            status=status.HTTP_201_CREATED
        )

    class InputGetSerializer(serializers.Serializer):
        department_id = serializers.IntegerField(
            required=True
        )

        def validate(self, attrs):
            department_id = attrs.get('department_id')
            department_qry = products_selectors.get_department_by_id(id=department_id)
            if not department_qry.exists():
                raise InventoryAPIException(ErrorCode.D01)
            return attrs

    class OutputGetProductSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        department_name = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField()
        code = serializers.CharField()
        cost = serializers.FloatField()
        price = serializers.FloatField()
        stock = serializers.IntegerField()

    def get(self, request):
        in_serializer = self.InputGetSerializer(data=request.query_params)
        in_serializer.is_valid(raise_exception=True)
        data = products_services.get_products_by_department_id(
            **in_serializer.validated_data
        )
        out_serializer = self.OutputGetProductSerializer(data=data, many=True)

        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.P00)

        return Response(
            out_serializer.data,
            status=status.HTTP_200_OK
        )


class ProductViewDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsPurchaseUser]

    class OutputGetProductSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        department_name = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField()
        code = serializers.CharField()
        cost = serializers.FloatField()
        price = serializers.FloatField()
        stock = serializers.IntegerField()

    def get(self, request, product_id):
        data = products_services.get_product_by_id(
            product_id=product_id
        )
        out_serializer = self.OutputGetProductSerializer(data=data)

        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.P00)

        return Response(
            out_serializer.data,
            status=status.HTTP_200_OK
        )

    class InputPutProductSerializer(serializers.Serializer):
        id = serializers.UUIDField(
            required=True
        )
        name = serializers.CharField(
            required=True
        )
        description = serializers.CharField(
            required=True
        )
        cost = serializers.FloatField(
            required=True
        )
        price = serializers.FloatField(
            required=False
        )
        stock = serializers.IntegerField(
            required=True
        )

        def validate(self, attrs):
            product_id = attrs.get('id')
            product_qry = products_selectors.get_product_by_id(id=product_id)
            if not product_qry.exists():
                raise InventoryAPIException(ErrorCode.P01)
            return attrs

    def put(self, request, product_id):
        in_serializer = self.InputPutProductSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = products_services.update_product(
            product_id=product_id,
            **in_serializer.validated_data
        )
        out_serializer = self.OutputGetProductSerializer(data=data)

        try:
            out_serializer.is_valid(raise_exception=True)
        except:
            raise InventoryAPIException(ErrorCode.P00)

        return Response(
            out_serializer.data,
            status=status.HTTP_202_ACCEPTED
        )
