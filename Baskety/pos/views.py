from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
from .models import Transaction, TransactionItem, Slide
from products.models import Product, Category
from inventory.models import StockMovement

class POSView(LoginRequiredMixin, TemplateView):
    template_name = 'pos/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Preload products for JS search (or implementation via API search for large datasets)
        # For small store, bootstrapping generic products list is fine.
        products_data = []
        for p in Product.objects.filter(is_active=True):
            products_data.append({
                'id': p.id,
                'name': p.name,
                'sku': p.sku,
                'price': float(p.selling_price),
                'stock': p.current_stock,
                'category_id': p.category_id,
                'image_url': p.image.url if p.image else None,
                'stock_status': p.stock_status
            })
        context['products_json'] = json.dumps(products_data)
        return context

class CustomerDisplayView(TemplateView):
    template_name = 'pos/customer_display.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = Slide.objects.filter(is_active=True)
        return context

@csrf_exempt
def process_checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            payment_info = data.get('payment', {})
            
            if not items:
                return JsonResponse({'success': False, 'message': 'Cart is empty'})

            with transaction.atomic():
                # 1. Create Transaction
                txn = Transaction.objects.create(
                    cashier=request.user if request.user.is_authenticated else None,
                    total_amount=data.get('total_amount', 0),
                    tax_amount=data.get('tax_amount', 0),
                    payment_method=payment_info.get('method', 'cash'),
                    amount_paid=payment_info.get('amount_paid', 0),
                    change_given=payment_info.get('change', 0),
                    status='completed'
                )

                # 2. Add Items & Update Stock
                for item in items:
                    product = get_object_or_404(Product, id=item['id'])
                    qty = int(item['qty'])
                    
                    TransactionItem.objects.create(
                        transaction=txn,
                        product=product,
                        quantity=qty,
                        unit_price=item['price'],
                        subtotal=qty * float(item['price'])
                    )

                    # Update Stock via StockMovement
                    # Note: Signal on StockMovement will update Product.current_stock
                    StockMovement.objects.create(
                        product=product,
                        movement_type='sale',
                        quantity=-qty, # Sale implies reduction
                        reason=f"Sale #{txn.id}",
                        user=request.user if request.user.is_authenticated else None
                    )
            
            return JsonResponse({'success': True, 'transaction_id': txn.id})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def receipt_view(request, txn_id):
    transaction = get_object_or_404(Transaction, id=txn_id)
    return render(request, 'pos/receipt.html', {'transaction': transaction})
