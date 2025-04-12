class XForwardedForMiddleware():
    def process_request(self, request):
        if 'x-forwarded-for' in request.headers:
            request.META['REMOTE_ADDR'] = request.headers['x-forwarded-for'].split(",")[0].strip()
        return None
