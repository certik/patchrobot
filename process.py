import cPickle

def group_messages(l):
    return [l]

l = cPickle.load(open("emails"))
for e in l:
    print "%s" % (e["subject"])
l = group_messages(l)
for group in l:
    print "-"*40
    for e in group:
        print "%s" % (e["subject"])
