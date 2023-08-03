# trade/models.py
from django.db import models

# Create your models here.



class Transaction(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    quantity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.quantity} {self.symbol} at ${self.price}"

class Balance(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return f"Balance: ${self.amount:.2f}"


class Trade(models.Model):
    trade_id = models.BigIntegerField(primary_key=True)
    symbol = models.CharField(max_length=10, default='')
    price = models.DecimalField(max_digits=15, decimal_places=8)
    quantity = models.DecimalField(max_digits=15, decimal_places=8)
    quote_quantity = models.DecimalField(max_digits=15, decimal_places=8)
    timestamp = models.BigIntegerField()
    is_buyer_maker = models.BooleanField()
    is_best_match = models.BooleanField()

    def __str__(self):
        return f"Trade ID: {self.trade_id},  Symbol: {self.symbol},  Price: {self.price}, Quantity: {self.quantity}"

