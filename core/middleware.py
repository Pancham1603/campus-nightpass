# middleware.py
from django.shortcuts import redirect

class RedirectUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.user_type == 'security':
            return redirect('/access')

        # Continue with the normal request/response cycle
        response = self.get_response(request)
        return response
