from django.contrib import admin
from .models import Thread, Message, Profile
# Register your models here.
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(Profile)

