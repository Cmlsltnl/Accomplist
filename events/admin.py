from events.models import *
from django.contrib import admin

class InstanceAdmin(admin.ModelAdmin):
      pass
admin.site.register(Instance, InstanceAdmin)

class EventAdmin(admin.ModelAdmin):
      list_display=('title','user')
      list_filter=('user',)
      search_fields=('title',)
admin.site.register(Event, EventAdmin)

class TagAdmin(admin.ModelAdmin):
      pass
admin.site.register(Tag, TagAdmin)

class UserProfileAdmin(admin.ModelAdmin):
      pass
admin.site.register(UserProfile, UserProfileAdmin)
