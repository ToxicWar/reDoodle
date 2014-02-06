# coding: utf-8
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from redoodle.models import Room, Chain
from .serializers import RoomListSerializer, RoomDetailSerializer, ChainListSerializer, ChainDetailSerializer, ChainCreateSerializer


class RoomList(ListCreateAPIView):
    model = Room
    serializer_class = RoomListSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            room, created = Room.objects.get_or_create(name=serializer.data['name'])
            headers = self.get_success_headers(serializer.data)
            if not created:
                return Response('The room is already created', status=status.HTTP_400_BAD_REQUEST, headers=headers)
            return Response(status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

room_list = RoomList.as_view()


class RoomDetail(RetrieveAPIView):
    model = Room
    serializer_class = RoomDetailSerializer

room_detail = RoomDetail.as_view()


class ChainList(ListCreateAPIView):
    model = Chain
    serializer_class = ChainListSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'

    def create(self, request, *args, **kwargs):
        serializer = ChainCreateSerializer(data=request.DATA)

        if serializer.is_valid():
            # I'm so sorry!
            try:
                room_id = int(serializer.data['room'])
            except ValueError as e:
                room, _ = Room.objects.get_or_create(name=serializer.data['room'])
            else:
                try:
                    room = Room.objects.get(id=room_id)
                except Room.DoesNotExist as e:
                    return Response('Room not found', status=status.HTTP_400_BAD_REQUEST)

            chain, created = room.chain_set.get_or_create(name=serializer.data['name'])
            headers = self.get_success_headers(serializer.data)
            if not created:
                return Response('The chain is already created', status=status.HTTP_400_BAD_REQUEST, headers=headers)
            return Response(status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

chain_list = ChainList.as_view()


class ChainDetail(RetrieveAPIView):
    model = Chain
    serializer_class = ChainDetailSerializer

chain_detail = ChainDetail.as_view()
