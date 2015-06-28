# coding: utf-8
from django.http import HttpResponse
from django.views.generic import View


class TestView(View):
    def get(self, request, *kwargs):
        return HttpResponse('OK')
test = TestView.as_view()
