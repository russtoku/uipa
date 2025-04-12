from django.contrib import admin

from .models import FoiRequestFollower


@admin.register(FoiRequestFollower)
class FoiRequestFollowerAdmin(admin.ModelAdmin):
    pass

