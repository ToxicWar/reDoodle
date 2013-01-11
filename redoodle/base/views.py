# coding: utf-8
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from redoodle.base.models import Chain, Room
from redoodle.base.forms import AddRoomForm, AddChainInRoom
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from redoodle.settings import PATH_ROOMS
import os


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
    try:
        image_name = len(os.listdir(PATH_ROOMS + room + '/' + chain + '/')) - 1
    except OSError:
        try:
            os.mkdir(PATH_ROOMS + room)
        except:
            pass
        os.mkdir(PATH_ROOMS + room + '/' + chain)
        image_name = len(os.listdir(PATH_ROOMS + room + '/' + chain + '/')) - 1
    return direct_to_template(request, 'editor.html', {'room': room, 'chain': chain, 'image_name': image_name})


def add_room(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            r1, r2 = Room.objects.get_or_create(name=room_name)
            if r2 is True:
                os.mkdir(PATH_ROOMS + room_name)
            return redirect('/' + room_name + '/')
        else:
            return index(request, form)
    return redirect('index')


def add_chain(request):
    if request.method == 'POST':
        form = AddChainInRoom(request.POST)
        if form.is_valid():
            room_name = form.data['room_name']
            chain_name = form.data['chain_name']
            room = Room.objects.get(name=room_name)
            r1, r2 = room.chain_set.get_or_create(name=chain_name)
            if r2 is True:
                os.mkdir(PATH_ROOMS + room_name + '/' + chain_name)
            return redirect('/' + room_name + '/' + chain_name + '/')
        else:
            return room(request, room_name, form)
    return redirect('/' + room_name + '/')


@csrf_exempt
def save_image(request):
    if request.is_ajax():
        if request.method == 'POST':
            data = request.POST['base64']
            room_name = request.POST['room']
            chain_name = request.POST['chain']
            print 'room name: ' + room_name + ', chain name: ' + chain_name
            message = 'Image sended.'
            image_name = len(os.listdir(PATH_ROOMS + room_name + '/' + chain_name + '/'))
            print 'open file ' + str(image_name) + '.png'
            f = open(PATH_ROOMS + room_name + '/' + chain_name + '/' + str(image_name) + '.png', "wb")
            try:
                data = data.strip('data:image/png;base64')
                imgData = b64decode(data)
                f.write(imgData)
            except:
                print 'Fail save image.'
                message = 'Fail save image.'
            f.close()
            print 'close file'
        else:
            message = 'Fail save image.'
    else:
        return HttpResponse(status=403)
    return HttpResponse(message)


def like(request):
    if request.is_ajax():
        if request.method == 'GET':
            chain_name = request.GET['chain']
            like = request.GET['like']
            print 'AJAX request ' + chain_name + ' ' + str(like)
            chain = Chain.objects.get(name=chain_name)
            if like == 'True':
                chain.like()
            else:
                chain.dislike()
            chain.save()
            message = chain.likes
    else:
        return HttpResponse(status=403)
    return HttpResponse(message)
