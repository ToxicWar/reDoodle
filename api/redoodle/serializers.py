# coding: utf-8
from django.contrib.sites.models import Site
from redoodle.models import Room, Chain, Image
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, Serializer


class ImageSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')

    class Meta:
        model = Image
        fields = ('id', 'image')

    def get_image(self, obj):
        image_url = 'http://{0}{1}'.format(Site.objects.get_current().domain, obj.image.url)
        return image_url


class ChainListSerializer(ModelSerializer):
    room = SerializerMethodField('get_room')
    image_set = ImageSerializer(many=True)

    class Meta:
        model = Chain
        fields = ('id', 'name', 'likes', 'room', 'image_set', 'is_blocked')

    def get_room(self, obj):
        return obj.room.name


class ChainCreateSerializer(Serializer):
    name = CharField(max_length=255)
    room = CharField(max_length=255)


class ChainDetailSerializer(ModelSerializer):
    room = SerializerMethodField('get_room')
    image_set = ImageSerializer(many=True)

    class Meta:
        model = Chain
        fields = ('id', 'name', 'likes', 'image_set', 'is_blocked')

    def get_room(self, obj):
        return obj.room.name


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')


class RoomDetailSerializer(ModelSerializer):
    chain_set = ChainDetailSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'chain_set')
