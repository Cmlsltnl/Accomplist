from django.db import models
from django.contrib.auth.models import User


class Wonderevent(models.Model):
      title = models.CharField(max_length = 100)
      def __unicode__ (self):
          return self.title

class Event(models.Model):
      title = models.ForeignKey(Wonderevent)
      date = models.DateTimeField()
      description = models.TextField()
      user = models.ForeignKey(User)
      def __unicode__(self):
          return unicode(self.title)
