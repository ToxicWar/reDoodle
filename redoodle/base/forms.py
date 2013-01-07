from django import forms


class AddRoomForm(forms.Form):
    room_name = forms.CharField(label = 'Room name')


class AddChainInRoom(forms.Form):
    chain_name = forms.CharField(label = 'Chain room')
