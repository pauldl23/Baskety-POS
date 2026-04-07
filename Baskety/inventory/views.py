from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.decorators import RoleRequiredMixin
from django.db.models import Sum, F, FloatField
from products.models import Product, Category
from .models import StockMovement
from django.urls import reverse_lazy
from django.contrib import messages

class InventoryDashboardView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = ['admin', 'manager']
    model = Product
    template_name = 'inventory/dashboard.html'
    context_object_name = 'products'
    # paginate_by = 50

    # def get_queryset(self):
    #     queryset = Product.objects.all().select_related('category')
    #     category = self.request.GET.get('category')
    #     status = self.request.GET.get('status')
    #     q = self.request.GET.get('q')

    #     if category:
    #         queryset = queryset.filter(category_id=category)
        
    #     if q:
    #         queryset = queryset.filter(name__icontains=q)

    #     if status == 'critical':
    #         queryset = queryset.filter(current_stock__lte=F('reorder_level'), current_stock__gt=0)
    #     elif status == 'low':
    #         queryset = queryset.filter(current_stock__gt=F('reorder_level'), current_stock__lte=F('reorder_level') + 50)
    #     elif status == 'out':
    #         queryset = queryset.filter(current_stock__lte=0)
    #     elif status == 'in':
    #         queryset = queryset.filter(current_stock__gt=F('reorder_level') + 50)

    #     return queryset.order_by('name')

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category')
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        q = self.request.GET.get('q')

        if category:
            queryset = queryset.filter(category_id=category)
        
        if q:
            # CHANGED: Added Q object to search both name AND sku
            from django.db.models import Q
            queryset = queryset.filter(Q(name__icontains=q) | Q(sku__icontains=q))

        if status == 'critical':
            queryset = queryset.filter(current_stock__lte=F('reorder_level'), current_stock__gt=0)
        # ... rest of status logic ...

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Summary Cards
        context['total_products'] = Product.objects.count()
        context['low_stock_count'] = Product.objects.filter(current_stock__lte=F('reorder_level'), current_stock__gt=0).count()
        context['out_of_stock_count'] = Product.objects.filter(current_stock__lte=0).count()
        # Calculate total value
        total_value = Product.objects.aggregate(
            total=Sum(F('current_stock') * F('selling_price'), output_field=FloatField())
        )['total'] or 0
        context['total_stock_value'] = round(total_value, 2)
        
        context['categories'] = Category.objects.all()
        return context

class StockAdjustmentView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['admin', 'manager']
    model = StockMovement
    fields = ['product', 'movement_type', 'quantity', 'reason']
    template_name = 'inventory/stock_adjustment.html'
    success_url = reverse_lazy('inventory:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Stock adjusted successfully.")
        return super().form_valid(form)
