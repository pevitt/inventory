from enum import Enum
from rest_framework import status
from rest_framework.exceptions import APIException


class ErrorCode(Enum):
    E00 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="An unexpected error occurred, try again"
    )
    C01 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Email is already used"
    )
    C02 = dict(
        status=status.HTTP_404_NOT_FOUND,
        message="User account is disabled."
    )
    C03 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Unable to log in with provided credentials."
    )
    C04 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Must include email and password."
    )
    D00 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="An unexpected error occurred while update Department."
    )
    D01 = dict(
        status=status.HTTP_404_NOT_FOUND,
        message="Department does not exist."
    )
    P00 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="An unexpected error occurred while update Product."
    )
    P01 = dict(
        status=status.HTTP_404_NOT_FOUND,
        message="Product does not exist."
    )
    P02 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Product already exist."
    )
    O00 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="An unexpected error occurred while create Order."
    )
    OP0 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="An unexpected error occurred while create Order."
    )
    OP1 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Quantity must be greater then 0."
    )
    OP3 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Cost must be greater then 0."
    )
    OP2 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Quantity for product is not available."
    )
    S00 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="An unexpected error occurred while create Sale Order."
    )
    S01 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Quantity must be greater then 0."
    )
    S02 = dict(
        status=status.HTTP_400_BAD_REQUEST,
        message="Quantity for product is not available."
    )

    @classmethod
    def get_by_message(cls, message: str):
        try:
            return next(
                error for error in cls
                if error.value['message'] == message
            )
        except (Exception,):
            return cls.E00

    @classmethod
    def get_by_code(cls, code: str):
        try:
            return next(
                error for error in cls
                if error.name == code
            )
        except (Exception,):
            return cls.E00


class InventoryAPIException(APIException):
    def __init__(
            self,
            error_code: ErrorCode = None,
            message: str = None
    ):
        error = error_code
        if message:
            error = ErrorCode.get_by_message(message)
        data = error.value
        self.status_code = data['status']
        super().__init__(detail=data['message'])

