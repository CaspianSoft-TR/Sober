from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            response.data['detail'] = 'Sorğunun metodu düzgün deyil'
        if response.status_code == status.HTTP_404_NOT_FOUND:
            response.data['detail'] = 'Sorğunuza cavab tapılmadı!'
    return response
