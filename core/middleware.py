# middleware.py
from django.shortcuts import redirect

class RedirectUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if their username is a specific value
        if (
            request.user.is_authenticated
            and request.user.user_type == 'security' and request.path not in ['/access', '/access/', '/logout', '/logout/', '/hostel', '/hostel/']
        ):
            return redirect('/access')

        # Continue with the normal request/response cycle
        response = self.get_response(request)
        return response
