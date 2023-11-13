from django.shortcuts import render
from rest_framework import permissions
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.exceptions import InventoryAPIException, ErrorCode

from django_apps.authentication import selectors as users_selectors
from django_apps.authentication import services as users_services

from django_apps.authentication.backends import EmailPasswordAuthBackend


# Create your views here.
class SignUPView(APIView):
    permission_classes = (permissions.AllowAny,)

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(
            max_length=100
        )
        last_name = serializers.CharField(
            max_length=100
        )
        role = serializers.CharField(
            max_length=20
        )
        password = serializers.CharField()

        def validate_email(self, data):
            email = data.lower()
            user = users_selectors.filter_user_by_email(
                email=email
            )
            if user.exists():
                raise InventoryAPIException(ErrorCode.C01)
            return email

        def validate(self, data):
            first_name = data['first_name']

            last_name = data['last_name']
            username = '%s.%s' % (first_name.lower(), last_name.lower())
            username = '{:.29}'.format(username)

            counter = users_selectors.filter_by_names(
                first_name=first_name,
                last_name=last_name
            ).count()

            if counter > 0:
                username += '%s' % (counter + 1)
            data['username'] = username
            return data

    def post(self, request):
        in_serializer = self.InputSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)

        try:
            data = users_services.create_user(
                **in_serializer.validated_data
            )
        except:
            raise InventoryAPIException(ErrorCode.C02)

        return Response(
            {},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(
            max_length=100,
            required=True
        )
        password = serializers.CharField(
            max_length=100,
            required=True
        )

        def validate(self, data):
            email = data['email'].lower()
            password = data['password']
            backend = EmailPasswordAuthBackend()
            user = backend.authenticate(
                email=email,
                password=password
            )
            if user is None:
                raise InventoryAPIException(ErrorCode.C03)
            data['user'] = user
            return data

    def post(self, request):
        in_serializer = self.InputSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        user = in_serializer.validated_data['user']
        data = {}
        try:
            data = users_services.get_token(
                user=user
            )
        except:
            raise InventoryAPIException(ErrorCode.C04)

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )