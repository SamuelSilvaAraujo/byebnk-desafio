from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import *


class CreatedAssetView(CreateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = CreatedAssetSerializer


class ListingAllAssetView(ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ListingAssetsSerializer

    def get_queryset(self):
        mode_filter = self.request.query_params.get('mode_filter')
        q_objects = Q()

        if mode_filter:
            q_objects.add(Q(mode=mode_filter), Q.AND)

        qs = Asset.objects.filter(q_objects)
        return qs


class CreatedTransactionView(CreateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = CreatedTransactionSerializer


class PortfolioView(ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Asset.objects.filter(transactions__created_by=self.request.user)
