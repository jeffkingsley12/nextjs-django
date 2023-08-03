from django.contrib import admin

# Register your models here.

from .models import Transaction, Balance, Trade

# Register Transaction and Balance models in the Django admin
admin.site.register(Transaction)
admin.site.register(Balance)
admin.site.register(Trade)

