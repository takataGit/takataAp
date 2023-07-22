from django.contrib import admin
from .models import Log,Category
from django.contrib.auth.models import Group


admin.site.register(Log)
admin.site.register(Category)
admin.site.unregister(Group)
