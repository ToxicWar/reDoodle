# coding: utf-8
from django.contrib import admin
from redoodle.models import Room, Chain, Image


class ChainAdmin(admin.ModelAdmin):
    list_display = ('name', 'likes', 'room')
    search_fields = ('name',)
    list_filter = ('room',)


admin.site.register(Room)
admin.site.register(Chain, ChainAdmin)
admin.site.register(Image)
