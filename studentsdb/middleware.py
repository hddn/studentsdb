from datetime import datetime

from django.http import HttpResponse


class RequestTimeMiddleware(object):
    """Displays request time on the page"""

    def process_request(self, request):
        request.start_time = datetime.now()
        return

    def process_response(self, request, response):
        if not hasattr(request, 'start_time'):
            return response

        request.end_time = datetime.now()
        if 'text/html' in response.get('Content-Type', ''):
            response.write('<br>Request took: %s' % str(
                request.end_time - request.start_time))
        return response

    def process_view(self, request, view, args, kwargs):
        return

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)
