from django.urls import path
from .views import POSView, process_checkout, receipt_view

app_name = 'pos'

urlpatterns = [
    path('', POSView.as_view(), name='index'),
    path('checkout/', process_checkout, name='checkout'),
    path('receipt/<int:txn_id>/', receipt_view, name='receipt'),
]
