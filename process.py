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

def try_parent(parent_id):
    try:
        c = Message.objects.get(message_id__exact=parent_id)
    except Message.DoesNotExist:
        c = None
    return c

def try_child(parent_id):
    try:
        c = Message.objects.get(parent_id__exact=parent_id)
    except Message.DoesNotExist:
        c = None
    return c

l = cPickle.load(open("emails"))
for e in l:
    sub = e["subject"]
    if sub.startswith("Re: "):
        sub = sub[4:]
    print sub
    m = Message(sender = e["from"], date=e["date"],
            subject = e["subject"], body = e["body"],
            message_id=e["ID"],
            )
    if e["parent"]:
        m.parent_id=e["parent"]
    c = try_parent(e["parent"])
    if c:
        m.parent = c.id
        m.patch = c.patch
        m.save()
        c = try_child(m.message_id)
        if c:
            # join the issues
            print "joining issues"
            c.parent = m.id
            c.save()
            p = Patch.objects.get(id__exact=m.patch.id)
            for x in p.message_set.all():
                x.patch = c.patch
                x.save()
            i = p.issue
            p.delete()
            i.delete()

    else:
        c = try_child(e["ID"])
        if c:
            print "WARNING: this was never tested, please check,"
            print "that all is ok and then remove this message",m.subject
            m.parent = 0
            m.patch = c.patch
            c.parent = m.id
            c.save()
            m.save()
        else:
            c = Message.objects.all()
            i = Issue()
            i.save()
            p = Patch(issue=i, subject=sub)
            p.save()
            m.parent = 0
            m.patch = p
            m.save()
