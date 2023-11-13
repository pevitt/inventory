from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from utils.exceptions import InventoryAPIException, ErrorCode
from django_apps.products import selectors as products_selectors
from django_apps.products import services as products_services
from django_apps.authentication.permissions import IsAdminUser, IsPurchaseUser


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