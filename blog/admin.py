from django.contrib import admin
from .models import Post, ThreadModel, Notification

# Register your models here.
admin.site.register(Post)
admin.site.register(ThreadModel)
admin.site.register(Notification)


