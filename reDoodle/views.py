# coding: utf-8
# from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import Chain


def index(request):
    chainsInDefaultRoom = Chain.objects.filter(room__name='default')
    return render_to_response('reDoodle.html', {'chainsInDefaultRoom': chainsInDefaultRoom})


def room(request, room):
    chainInRoom = Chain.objects.filter(room__name=room)
    return render_to_response('room.html', {'room': room, 'chainInRoom': chainInRoom})


def editor(request, room, chain):
    return render_to_response('editor.html', {'room': room, 'chain': chain})
