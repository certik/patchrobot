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

def group_messages(l):
    return [[[x]] for x in l]

l = cPickle.load(open("emails"))
l = group_messages(l)
for issue in l:
    i = Issue()
    i.save()
    print i
    for patch in issue:
        p = Patch(issue=i)
        p.save()
        for e in patch:
            m = Message(patch=p, _from = e["from"], date=e["date"],
                    subject = e["subject"], body = e["body"])
            m.save()
