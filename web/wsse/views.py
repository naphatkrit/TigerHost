from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from wsse.decorators import check_wsse_token

# Create your views here.


@check_wsse_token
def test_view(request):
    return HttpResponse(request.user.username)


@method_decorator(check_wsse_token, name='dispatch')
class TestView(View):
    def get(self, request):
        return HttpResponse(request.user.username)
