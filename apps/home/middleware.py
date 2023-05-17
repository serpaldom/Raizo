from django.utils import timezone

class UserTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la zona horaria configurada en el navegador o en la computadora del usuario
        user_timezone = request.headers.get('timezone')  # Asegúrate de que el encabezado 'timezone' se esté enviando desde el cliente

        if user_timezone:
            timezone.activate(user_timezone)  # Establecer la zona horaria configurada en el navegador o en la computadora del usuario

        response = self.get_response(request)

        return response
