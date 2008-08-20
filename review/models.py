from django.db import models
from django.contrib import admin

class Issue(models.Model):
    """
    Issue consists of one ore more Patches.
    """
    pass

class Patch(models.Model):
    """
    Patch contains one or more Messages.
    """
    issue = models.ForeignKey(Issue)

class Message(models.Model):
    """
    Individual email message.

    Each message belongs to some patch.
    """
    patch = models.ForeignKey(Patch)
    _from = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    #date = models.DateTimeField('message date')
    date = models.CharField(max_length=100)
    body = models.CharField(max_length=10000)

admin.site.register(Issue)
admin.site.register(Patch)
admin.site.register(Message)
