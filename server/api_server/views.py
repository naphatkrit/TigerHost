# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import wsse.utils


@login_required
def api_key_view(request):
    # TODO make this pretty
    secret = wsse.utils.get_secret(request.user.username)
    return HttpResponse(secret)
