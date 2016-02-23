from django.http import HttpResponse

from wsse.decorators import check_wsse_token

# Create your views here.
@check_wsse_token
def test_view(request):
    return HttpResponse(request.user.username)
