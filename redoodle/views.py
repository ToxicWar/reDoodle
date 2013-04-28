# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from redoodle.models import Chain, Room
from redoodle.forms import AddRoomForm, AddChainInRoom, SaveImage
import os


class IndexView(TemplateView):
    template_name = 'reDoodle.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['chainsInDefaultRoom'] = Chain.objects.filter(room__name='default')
        context['form'] = kwargs.get('form', AddRoomForm())
        #remove from here
        """if 'request' in context:
            print "request in context"
        else:
            print "request not in context"
            context['request'] = lambda: None
        context['request'].login_form = "form from index" #remove it
        
        if hasattr(self.request, 'login_form'):
            print "fisr", self.request.login_form
        else:
            print "fnisr"
        self.request.login_form = "form from index2" """
        #to here
        # it sets login_form to request, later it is
        # overwritten by context processor (possible data transfer)
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
            # create room folder
            os.mkdir(os.path.join('redoodle/static/room/', context['room']))
        except OSError:
            try:
                # create chain folder
                os.mkdir(os.path.join('redoodle/static/room/', context['room'], context['chain']))
            except OSError:
                # getting image name
                context['image_name'] = len(os.listdir(os.path.join('redoodle/static/room/', context['room'], context['chain']))) - 1
        return context

editor = EditorView.as_view()


class AddRoomView(FormView):
    form_class = AddRoomForm

    def form_valid(self, form):
        room_name = form.cleaned_data['room_name']
        # r1 - object, r2 - created
        r1, r2 = Room.objects.get_or_create(name=room_name)
        # if created room
        if r2 is True:
            # then created room folder
            os.mkdir(os.path.join('redoodle/static/room/', room_name))
        # success url - /room name/
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
            os.mkdir(os.path.join('redoodle/static/room/', room_name, chain_name))
        self.success_url = reverse_lazy('editor', kwargs={'room': room_name, 'chain': chain_name})
        return super(AddChainView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors)

add_chain = AddChainView.as_view()


class SaveImageView(FormView):
    form_class = SaveImage

    def form_valid(self, form):
        # result: 'Image sended.' or 'Fail save image.'
        result = form.save_image()
        return HttpResponse(result)

save_image = SaveImageView.as_view()


def like(request):
    if request.is_ajax():
        if request.method == 'GET':
            chain_name = request.GET['chain']
            like = request.GET['like']
            chain = Chain.objects.get(name=chain_name)
            user = request.user
            if like == 'True':
                chain.like(user)
            else:
                chain.dislike(user)
            chain.save()
            message = chain.likes
    else:
        return HttpResponse(status=403)
    return HttpResponse(message)
