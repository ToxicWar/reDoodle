# coding: utf-8
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from redoodle.base.models import Chain, Room
from redoodle.base.forms import AddRoomForm, AddChainInRoom


def index(request, form=None):
    chainsInDefaultRoom = Chain.objects.filter(room__name='default')
    if form == None:
        form = AddRoomForm()
    return direct_to_template(request, 'reDoodle.html', {'chainsInDefaultRoom': chainsInDefaultRoom, 'form': form})


def room(request, room, form=None):
    chainInRoom = Chain.objects.filter(room__name=room)
    if form == None:
        form = AddChainInRoom()
    return direct_to_template(request, 'room.html', {'room': room, 'chainInRoom': chainInRoom, 'form': form})


def editor(request, room, chain):
    return direct_to_template(request, 'editor.html', {'room': room, 'chain': chain})


def add_room(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            r1, r2 = Room.objects.get_or_create(name=form.cleaned_data['room_name'])
            return redirect('/%s/' % form.cleaned_data['room_name'])
        else:
            return index(request, form)
    return redirect('index')


def add_chain(request):
    if request.method == 'POST':
        form = AddChainInRoom(request.POST)
        if form.is_valid():
            room = Room.objects.get(name=form.data['room_name'])
            r1, r2 = room.chain_set.get_or_create(name=form.data['chain_name'], isBlocked=False)
            return redirect('/%s/%s/' % (form.data['room_name'], form.cleaned_data['chain_name']))
        else:
            return room(request, form.data['room_name'], form)
    return redirect('/%s/' % form.data['room_name'])
