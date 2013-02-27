# coding: utf-8
from django.views.generic.simple import direct_to_template


def graphics_editor(request):
    return direct_to_template(request, 'graphics_editor.html', {})
