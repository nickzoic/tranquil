"""Django support for Tranquil"""

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import json

def context_class_to_view(context_class):

    def view_function(request):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])

        content_type = request.META.get('CONTENT_TYPE').split(';')[0]
        if content_type != 'application/json':
            return HttpResponseBadRequest("bad content-type %s" % content_type)
        try:
            request_data = json.load(request)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        context = context_class(request)
        response_data = context.process(request_data)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
        )

    return view_function 
