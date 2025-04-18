from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView

from stocks.models import stockEntry, product, stockBunch
from ..serializers.stockEntrySerializers import BulkStockEntrySerializer, ProductListSerializer, StockBunchSerializer

from django.utils.timezone import now



class StockInView(CreateAPIView):
    serializer_class = BulkStockEntrySerializer
    queryset = BulkStockEntrySerializer.Meta.model.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            stockBunch_id = stockBunch.objects.create()
            serializer.context['stockBunch_id'] = stockBunch_id.id
            data = serializer.save()
            return Response({"status": "success",
            "message": "Stock Entry has been created successfully",
            "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Validation Error", "errors":serializer.errors[0]}, status=status.HTTP_400_BAD_REQUEST)


class StockBunchView(ListAPIView):

    serializer_class = StockBunchSerializer

    def get_queryset(self):
        stockBunch_id = stockBunch.objects.all()
        entries = stockEntry.objects.filter(stockBunch_id__in=stockBunch_id).order_by('-created_at')
        return entries

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        grouped_data = {}
        for entry in serializer.data:
            created_at = entry['created_at']
            if entry['deleted_at']:
                continue
            if created_at not in grouped_data:
                grouped_data[created_at] = []
            grouped_data[created_at].append({
                "id": entry["id"],
                "product_name": entry["product_name"],
                "batch_number": entry["batch_number"],
                "expiry_date": entry["expiry_date"],
                "quantity": entry["quantity"],
                "stockBunch_id": entry["stockBunch_id"],
            })
        response_data = [
            {
                "created_at": created_at,
                "data": grouped_data[created_at]
            }
            for created_at in grouped_data
        ]
        return Response(response_data, status=status.HTTP_200_OK)


class StockBunchDestroyView(DestroyAPIView):
    queryset = stockBunch.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            stockBunch_instance = self.get_object()
        except stockBunch.DoesNotExist:
            errors = {"stockBunch_id": "StockBunch with the given ID does not exist."}
            return Response(
                {"status": "error", "message": "Validation Error", "errors": errors},
                status=status.HTTP_404_NOT_FOUND
            )
        stockBunch_instance.deleted_at = now()
        stockBunch_instance.save()
        return Response({"status": "success",
            "message": "Stock Bunch deleted Successfully"},status=status.HTTP_204_NO_CONTENT)


class ProductListView(ListAPIView):

    serializer_class = ProductListSerializer
    queryset = product.objects.filter(deleted_at=None)