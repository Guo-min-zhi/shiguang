from django.contrib import admin
from .models import User, Authcode, AuthcodeHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Authcode)
admin.site.register(AuthcodeHistory)