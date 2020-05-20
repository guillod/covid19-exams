from django.utils.deprecation import MiddlewareMixin

# add username to request
class RemoteUserMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            response['X-Remote-User-Name'] = request.user.username
        return response
