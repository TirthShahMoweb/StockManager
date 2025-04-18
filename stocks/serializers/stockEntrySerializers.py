from rest_framework import serializers

from stocks.models import stockEntry, product, stockBunch

from datetime import date



class BulkStockEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = stockEntry
        fields = ['product', 'batch_number', 'expiry_date', 'quantity']

    def validate(self, data):
        if not product.objects.filter(id = data['product'].id).exists():
            raise serializers.ValidationError({
            "product_id": f"Product {data['product'].id} does not exist."
            })

        product_name = product.objects.filter(id = data['product'].id).values_list('product_name', flat=True).first()
        if data['expiry_date'] < date.today():
            raise serializers.ValidationError({
            "expiry_date": f"Expiry date must be greater than or equal to today's date in {product_name} ."
            })

        if not data['batch_number']:
            raise serializers.ValidationError({
                "batch_number": f"Batch number cannot be empty in {product_name}."
            })
        if data['batch_number'][:1] != '#':
            raise serializers.ValidationError({
                "batch_number": f"Batch number must start with '#' in {product_name}."
            })
        if not data['batch_number'][1:].isdigit():
            raise serializers.ValidationError({
                "batch_number": f"Batch number must contain only digits after '#' in {product_name}."
            })

        if data['quantity'] <= 0:
            raise serializers.ValidationError({
                "quantity": f"Quantity must be greater than 0 in {product_name}."
            })
        return data

    def create(self, validated_data):
        stockBunch_id = stockBunch.objects.filter(id=self.context.get('stockBunch_id')).first()
        stockEntry.objects.create(**validated_data, stockBunch_id=stockBunch_id)
        return validated_data


class StockBunchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name')
    created_at = serializers.DateTimeField(source = 'stockBunch_id.created_at')
    deleted_at = serializers.DateTimeField(source = 'stockBunch_id.deleted_at')

    class Meta:
        model = stockEntry
        fields = ('id', 'product_name', 'batch_number', 'expiry_date', 'quantity','stockBunch_id', 'created_at','deleted_at')

    def create(self, validated_data):
        stockBunch_instance = stockBunch.objects.create(**validated_data)
        return stockBunch_instance

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['id', 'product_name']