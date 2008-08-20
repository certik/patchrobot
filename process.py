#! /usr/bin/env python
import cPickle

import sys
sys.path.append("..")
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "patchrobot.settings"

from patchrobot.review.models import Issue, Patch, Message

print "deleting database"
Issue.objects.all().delete()
Patch.objects.all().delete()
Message.objects.all().delete()
print "adding messages"

l = cPickle.load(open("emails"))
for e in l:
    sub = e["subject"]
    if sub.startswith("Re: "):
        sub = sub[4:]
    print sub
    m = Message( sender = e["from"], date=e["date"],
            subject = e["subject"], body = e["body"])
    try:
        c = Message.objects.get(subject__exact=sub)
        m.patch = c.patch
    except Message.DoesNotExist:
        i = Issue()
        i.save()
        p = Patch(issue=i, subject=sub)
        p.save()
        m.patch = p
    m.save()
