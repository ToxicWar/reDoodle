from django import forms
from redoodle.settings import PATH_ROOMS
from base64 import b64decode
import os


class AddRoomForm(forms.Form):
    room_name = forms.CharField(label='Room name', max_length=255)


class AddChainInRoom(forms.Form):
    room_name = forms.CharField(required=True, widget=forms.HiddenInput())
    chain_name = forms.CharField(label='Chain room', max_length=255)


class SaveImage(forms.Form):
    base64 = forms.CharField(required=True)
    room = forms.CharField(required=True)
    chain = forms.CharField(required=True)

    def save_image(self):
        data = self.cleaned_data['base64']
        room_name = self.cleaned_data['room']
        chain_name = self.cleaned_data['chain']
        message = 'Image sended.'
        image_name = len(os.listdir(os.path.join(PATH_ROOMS, room_name, chain_name)))
        f = open(os.path.join(PATH_ROOMS, room_name, chain_name, str(image_name) + '.png'), "wb")
        try:
            data = data.strip('data:image/png;base64')
            imgData = b64decode(data)
            f.write(imgData)
        except:
            message = 'Fail save image.'
        f.close()
        return message
