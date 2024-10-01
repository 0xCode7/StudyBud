from django.contrib import admin
from .models import User, Room, Topic, Message
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'created')

admin.site.register(Room, RoomAdmin)   

# admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
