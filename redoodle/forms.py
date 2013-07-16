# coding: utf-8
from django.core.files.base import ContentFile
from django import forms
from base64 import b64decode
from redoodle.models import Chain, Image
import os


class AddRoomForm(forms.Form):
    room_name = forms.CharField(label='Room name', max_length=255)


class AddChainInRoom(forms.Form):
    # his first comment.
    # After a couple of minutes of hard brain work and loud keyboard
    # buttons clicks The First Comment was written!
    # Hete it is:
    # room name hidden field (data are substituted into views)
    # Althoug it may be better not to mix times togeter as Lutece did
    # and write someting like "data will be subsituted ... "
    #                      or "data is substituted"
    # we'll remain it as it is in memory of
    #            *** The Great Day Of The First 4ui Comment ***
    room_name = forms.CharField(required=True, widget=forms.HiddenInput())
    chain_name = forms.CharField(label='Chain room', max_length=255)


class SaveImage(forms.Form):
    base64 = forms.CharField(required=True)
    room = forms.CharField(required=True)
    chain = forms.CharField(required=True)

    def save_image(self):
        # major passed validation data
        data = self.cleaned_data['base64']
        room_name = self.cleaned_data['room']
        chain_name = self.cleaned_data['chain']
        chain = Chain.objects.get(name=chain_name)
        message = 'Image sended.'

        try:
            # decode base64 and save image
            data = data.strip('data:image/png;base64')
            img_data = b64decode(data)
            image = Image.objects.create(chain=chain)
            image.image = ContentFile(img_data, '%s.png' % (chain.image_set.count()))
            image.save()
        except: # TODO: Fix it
            # exception: Image not saved or data not decode
            message = 'Fail save image.'
        return message
