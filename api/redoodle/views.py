# coding: utf-8
from rest_framework.generics import ListAPIView, RetrieveAPIView
from redoodle.models import Room, Chain
from .serializers import RoomListSerializer, RoomDetailSerializer, ChainListSerializer, ChainDetailSerializer


class RoomList(ListAPIView):
    model = Room
    serializer_class = RoomListSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'

room_list = RoomList.as_view()


class RoomDetail(RetrieveAPIView):
    model = Room
    serializer_class = RoomDetailSerializer

room_detail = RoomDetail.as_view()


class ChainList(ListAPIView):
    model = Chain
    serializer_class = ChainListSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'

chain_list = ChainList.as_view()


class ChainDetail(RetrieveAPIView):
    model = Chain
    serializer_class = ChainDetailSerializer

chain_detail = ChainDetail.as_view()
