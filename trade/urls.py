# trade/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('trading/', views.trading_view, name='trading'),
    path('transaction-history/', views.transaction_history_view, name='transaction_history'),
    path('save_trade_data/<str:symbol>/', views.save_trade_data, name='save_trade_data'),
]

