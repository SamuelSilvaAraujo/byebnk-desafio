from rest_framework.serializers import ModelSerializer

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
        instance = Asset.objects.create(**validated_data)
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
        instance = Transaction.objects.create(**validated_data)
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
