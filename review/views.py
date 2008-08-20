from django.shortcuts import render_to_response
from django.http import HttpResponse

from patchrobot.review.models import Issue, Patch

def index(request):
    issue_list = Issue.objects.all()
    return render_to_response('review/index.html', {'issue_list': issue_list})

def patch(request, patch_id):
    patch = Patch.objects.get(id__exact=patch_id)
    return render_to_response('review/patch.html', {'patch': patch})
