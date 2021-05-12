from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import *


class CreatedAssetView(CreateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = CreatedAssetSerializer


class ListingAssetView(ListAPIView):
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


class ListingTransactionView(ListAPIView):
    serializer_class = ListingTransactionSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        q_objects = Q(created_by=self.request.user)

        is_redemption_filter = self.request.query_params.get('is_redemption_filter')

        if is_redemption_filter:
            q_objects.add(Q(is_redemption=is_redemption_filter), Q.AND)

        qs = Transaction.objects.filter(q_objects)
        return qs
