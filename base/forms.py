from django import forms


class AddRoomForm(forms.Form):
    room_name = forms.CharField(label='Room name', max_length=255)


class AddChainInRoom(forms.Form):
    room_name = forms.CharField(required=True, widget=forms.HiddenInput())
    chain_name = forms.CharField(label='Chain room', max_length=255)


class SaveImage(forms.Form):
    pass
