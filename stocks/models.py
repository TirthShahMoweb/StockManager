from django.db import models
from utils.baseModel import BaseModel
# Create your models here.

class product(BaseModel):
    product_name = models.CharField(max_length=100)

class stockEntry(BaseModel):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=10)
    expiry_date = models.DateField()
    quantity = models.IntegerField()
    stockBunch_id = models.ForeignKey('stockBunch', on_delete=models.CASCADE, null=True, blank=True)

class stockBunch(BaseModel):
    ...