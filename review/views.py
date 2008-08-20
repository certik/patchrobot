from django.shortcuts import render_to_response
from django.http import HttpResponse

from patchrobot.review.models import Issue

def index(request):
    issue_list = Issue.objects.all()
    return render_to_response('review/index.html', {'issue_list': issue_list})

def issue(request, issue_id):
    return HttpResponse("Hello, world. You're at the poll index.")

def message(request, issue_id, message_id):
    return HttpResponse("Hello, world. You're at the poll index.")
