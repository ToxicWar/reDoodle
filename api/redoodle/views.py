# coding: utf-8
from rest_framework.generics import ListAPIView
from redoodle.models import Chain
from .serializers import ChainSerializer


class ChainList(ListAPIView):
    model = Chain
    serializer_class = ChainSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'

chain_list = ChainList.as_view()
