from tastypie.resources import ModelResource
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
    user = fields.ForeignKey(UserResource, 'user')
    title = fields.ForeignKey(InstanceResource, 'title')
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'

class SharedEventResource(ModelResource):
    class Meta:
	queryset = SharedEvent.objects.all()
	resource_name = 'sharedevent'

class TagResource(ModelResource):
    class Meta:
	queryset = Tag.objects.all()
	resource_name = 'tag'

class UserProfileResource(ModelResource):
    class Meta:
	queryset = UserProfile.objects.all()
	resource_name = 'userprofile'
