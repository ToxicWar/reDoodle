# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from base.models import Chain, Room
from base.forms import AddRoomForm, AddChainInRoom
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from redoodle.settings import PATH_ROOMS
import os


class IndexView(TemplateView):
    template_name = 'reDoodle.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['chainsInDefaultRoom'] = Chain.objects.filter(room__name='default')
        context['form'] = kwargs.get('form', AddRoomForm())
        return context

index = IndexView.as_view()


class RoomView(TemplateView):
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room'] = kwargs['room']
        context['chainInRoom'] = Chain.objects.filter(room__name=context['room'])
        context['form'] = kwargs.get('form', AddChainInRoom())
        return context

room = RoomView.as_view()


class EditorView(TemplateView):
    template_name = 'editor.html'

    def get_context_data(self, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        context['room'] = kwargs['room']
        context['chain'] = kwargs['chain']
        # TODO: Transform to a nice design
        try:
            os.mkdir(os.path.join(PATH_ROOMS, context['room']))
        except OSError:
            try:
                os.mkdir(os.path.join(PATH_ROOMS, context['room'], context['chain']))
            except OSError:
                context['image_name'] = len(os.listdir(os.path.join(PATH_ROOMS, context['room'], context['chain']))) - 1
        return context

editor = EditorView.as_view()


class AddRoomView(FormView):
    form_class = AddRoomForm

    def form_valid(self, form):
        room_name = form.cleaned_data['room_name']
        r1, r2 = Room.objects.get_or_create(name=room_name)
        if r2 is True:
            os.mkdir(os.path.join(PATH_ROOMS, room_name))
        self.success_url = reverse_lazy('room', kwargs={'room': room_name})
        return super(AddRoomView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors)

add_room = AddRoomView.as_view()


class AddChainView(FormView):
    form_class = AddChainInRoom

    def form_valid(self, form):
        room_name = form.cleaned_data['room_name']
        chain_name = form.cleaned_data['chain_name']
        room = Room.objects.get(name=room_name)
        r1, r2 = room.chain_set.get_or_create(name=chain_name)
        if r2 is True:
            os.mkdir(os.path.join(PATH_ROOMS, room_name, chain_name))
        self.success_url = reverse_lazy('editor', kwargs={'room': room_name, 'chain': chain_name})
        return super(AddChainView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors)

add_chain = AddChainView.as_view()


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
