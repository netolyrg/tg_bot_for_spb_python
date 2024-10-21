from django.contrib import admin

from core.models import Profile, EventType, Slot

# Register your models here.
admin.site.register(Profile)
admin.site.register(EventType)
admin.site.register(Slot)