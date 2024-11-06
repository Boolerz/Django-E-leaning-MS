# custom_middleware.py
class CorrectContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.endswith('.css'):
            response['Content-Type'] = 'text/css'
        return response
