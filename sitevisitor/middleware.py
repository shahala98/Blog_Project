class NoCatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The main logic of the middleware
        try:
            response = self.get_response(request)
        except Exception as e:
            # Instead of catching the exception and handling it, we re-raise it
            raise e
        return response
