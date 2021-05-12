from django.db.models import Sum, DecimalField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Asset, Transaction


class CreatedAssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'name',
            'mode',
            'created_by',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Asset.objects.create(**validated_data, created_by=user)
        return instance


class ListingAssetsSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'id',
            'name',
            'mode',
        )


class CreatedTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'asset',
            'amount',
            'unit_price',
            'ip_address',
            'request_date',
            'is_redemption',
            'created_by',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Transaction.objects.create(**validated_data, created_by=user)
        return instance


class ListingTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'asset',
            'amount',
            'unit_price',
            'ip_address',
            'request_date',
            'is_redemption',
            'created_by',
        )


class PortfolioSerializer(ModelSerializer):
    transactions = ListingTransactionSerializer(many=True, read_only=True)
    balance = SerializerMethodField()

    class Meta:
        model = Asset
        fields = (
            'id',
            'name',
            'transactions',
            'balance',
        )

    def get_balance(self, obj):
        redemptions = obj.transactions \
                          .filter(is_redemption=True) \
                          .aggregate(total=Sum('id', field="unit_price * amount",
                                               output_field=DecimalField()))['total'] or 0
        investments = obj.transactions \
                          .filter(is_redemption=False) \
                          .aggregate(total=Sum('id', field="unit_price * amount",
                                               output_field=DecimalField()))['total'] or 0
        return investments - redemptions
