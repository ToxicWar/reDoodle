from django import forms


class AddRoomForm(forms.Form):
    room_name = forms.CharField(label='Room name', max_length=255)


class AddChainInRoom(forms.Form):
    # TODO(ToxicWar): Use hidden field and static information about the room
    room_name = forms.CharField(required=True, widget=forms.HiddenInput())
    chain_name = forms.CharField(label='Chain room', max_length=255)
