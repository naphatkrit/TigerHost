# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def token_generate_page(request):
    return HttpResponse('testing')
