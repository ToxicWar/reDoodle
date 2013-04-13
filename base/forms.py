from django import forms
from .conf import app_settings
from base64 import b64decode
import os


class AddRoomForm(forms.Form):
    room_name = forms.CharField(label='Room name', max_length=255)


class AddChainInRoom(forms.Form):
    # The day was coming to the end when 4ui припекло write some comments.
    # So he remembered all the разговорный he knew and started writing
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
        message = 'Image sended.'
        # image_name = number of files
        image_name = len(os.listdir(os.path.join(app_settings.PATH_ROOMS, room_name, chain_name)))
        # create and open file
        f = open(os.path.join(app_settings.PATH_ROOMS, room_name, chain_name, str(image_name) + '.png'), "wb")
        try:
            # decode base64 and save image
            data = data.strip('data:image/png;base64')
            imgData = b64decode(data)
            f.write(imgData)
        except:
            # exception: Image not saved or data not decode
            message = 'Fail save image.'
        f.close()
        return message
