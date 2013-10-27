# coding: utf-8
from django.contrib.sites.models import Site
from redoodle.models import Room, Chain, Image
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('name')


class ImageSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')

    class Meta:
        model = Image
        fields = ('id', 'image', 'ban')

    def get_image(self, obj):
        image_url = 'http://{0}{1}'.format(Site.objects.get_current().domain, obj.image.url)
        return image_url


class ChainSerializer(ModelSerializer):
    room = SerializerMethodField('get_room')
    image_set = ImageSerializer(many=True)

    class Meta:
        model = Chain
        fields = ('id', 'name', 'likes', 'is_blocked', 'room', 'image_set')

    def get_room(self, obj):
        return obj.room.name
