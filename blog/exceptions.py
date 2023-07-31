from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Özel hata mesajları veya HTTP durumu ekleyebilirsiniz
        response.data['detail'] = 'Bir hata oluştu.'

    return response
