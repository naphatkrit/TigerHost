# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import wsse.utils

from wsse.decorators import check_wsse_token


@login_required
def api_key_view(request):
    """This view returns the user's WSSE API key and is protected by authentication
    """
    secret = wsse.utils.get_secret(request.user.username)
    return HttpResponse(secret)


@check_wsse_token
def test_api_key(request):
    return HttpResponse('OK')
