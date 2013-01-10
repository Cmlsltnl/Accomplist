from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage



class Instance(models.Model):
      listitem = models.CharField(max_length = 100)
      def __unicode__(self):
          return self.listitem

class Event(models.Model):
      title = models.ForeignKey(Instance)
      description = models.TextField()
      user = models.ForeignKey(User)
      
      def __unicode__(self):
          return u'%s, %s' % (self.user.username, self.title.listitem) 

class Tag(models.Model):
      name = models.CharField(max_length=64, unique=True)
      events = models.ManyToManyField(Event)
      def __unicode__(self):
            return self.name

class SharedEvent(models.Model):
      event = models.ForeignKey(Event, unique=True)
      date = models.DateTimeField(auto_now_add=True)
      votes = models.IntegerField(default=1)
      users_voted = models.ManyToManyField(User)
      def __unicode__(self):
          return u'%s, %s' % (self.event, self.votes)

class UserProfile(models.Model):
      user = models.ForeignKey(User)
      firstName = models.CharField(max_length= 100)
      lastName = models.CharField(max_length= 100)
      tagline = models.CharField(max_length = 100)
      def __unicode__(self):
          return u'%s, %s' % (self.firstName, self.lastName)

