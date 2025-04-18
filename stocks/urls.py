from django.urls import path,include
from .views import stockEntryViews

urlpatterns = [
    path('StockInView', stockEntryViews.StockInView.as_view(), name='StockInView'),
    path('StockBunchView', stockEntryViews.StockBunchView.as_view(), name='StockBunchView'),
    path('StockBunchDestroyView/<int:pk>', stockEntryViews.StockBunchDestroyView.as_view(), name='StockBunchDestroyView'),
    path('ProductListView', stockEntryViews.ProductListView.as_view(), name='ProductListView'),
]
