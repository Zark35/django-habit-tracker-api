from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


class APIException(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(APIException):
    """Custom validation error."""
    
    def __init__(self, message, code='validation_error'):
        super().__init__(message, code, status.HTTP_400_BAD_REQUEST)


class AuthenticationError(APIException):
    """Custom authentication error."""
    
    def __init__(self, message, code='authentication_failed'):
        super().__init__(message, code, status.HTTP_401_UNAUTHORIZED)


class PermissionError(APIException):
    """Custom permission error."""
    
    def __init__(self, message, code='permission_denied'):
        super().__init__(message, code, status.HTTP_403_FORBIDDEN)


class NotFoundError(APIException):
    """Custom not found error."""
    
    def __init__(self, message, code='not_found'):
        super().__init__(message, code, status.HTTP_404_NOT_FOUND)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    Handles both DRF exceptions and custom API exceptions.
    """
    response = drf_exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, APIException):
            return Response(
                {
                    'error': {
                        'message': exc.message,
                        'code': exc.code,
                    }
                },
                status=exc.status_code
            )
    
    return response
