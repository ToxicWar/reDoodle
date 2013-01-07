# coding: utf-8
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from redoodle.base.models import Chain
from redoodle.base.forms import AddRoomForm, AddChainInRoom


def index(request):
    chainsInDefaultRoom = Chain.objects.filter(room__name='default')
    form = AddRoomForm()
    return direct_to_template(request, 'reDoodle.html', {'chainsInDefaultRoom': chainsInDefaultRoom, 'form': form})


def room(request, room):
    chainInRoom = Chain.objects.filter(room__name=room)
    form = AddChainInRoom()
    return direct_to_template(request, 'room.html', {'room': room, 'chainInRoom': chainInRoom, 'form': form})


def editor(request, room, chain):
    return direct_to_template(request, 'editor.html', {'room': room, 'chain': chain})


def add_room(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            return redirect('/%s/' % form.cleaned_data['room_name'])
    return redirect('index')


def add_chain(request):
    if request.method == 'POST':
        form = AddChainInRoom(request.POST)
        if form.is_valid():
            return redirect('/%s/%s/' % (form.data['room_name'], form.cleaned_data['chain_name']))
    return redirect('/%s/' % form.data['room_name'])
