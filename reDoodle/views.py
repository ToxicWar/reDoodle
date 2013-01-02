# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime


def hello(request):
    return HttpResponse('Hello world')


def current_datetime(request):
    now = datetime.datetime.now()
    html = '<h1>%s.</h1>' % now
    return HttpResponse(html)


def room(request, room):
    return render_to_response('room.html', {'room': room})


def chain(request, room, chain):
    html = '<h1>Room: %s,</h1><h2> Chain: %s</h2>' % (room, chain)
    return HttpResponse(html)
