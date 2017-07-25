from django.utils.translation import LANGUAGE_SESSION_KEY


class SetUserLanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_user = request.user
        if hasattr(current_user, 'pigeonuser'):
            language = current_user.pigeonuser.language or 'fr'
            request.session[LANGUAGE_SESSION_KEY] = language
        response = self.get_response(request)
        return response
