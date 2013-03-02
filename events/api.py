from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie import fields
from events.models import *

class InstanceResource(ModelResource):
    class Meta:
	queryset = Instance.objects.all()
	resource_name = 'title'

class UserResource(ModelResource):
    class Meta:
	queryset = User.objects.all()
	resource_name = 'user'

class EventResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user',full=True)
    title = fields.ForeignKey(InstanceResource, 'title',full=True)
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
	excludes = ['resource_uri','date_joined','last_login','last_name', 'first_name','password','is_active','is_staff','is_superuser']
        authentication = BasicAuthentication()

class SharedEventResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event',full=True)
    class Meta:
	queryset = SharedEvent.objects.order_by('-votes')
	resource_name = 'sharedevent'	

class TagResource(ModelResource):
    class Meta:
	queryset = Tag.objects.all()
	resource_name = 'tag'

class UserProfileResource(ModelResource):
    class Meta:
	queryset = UserProfile.objects.all()
	resource_name = 'userprofile'
