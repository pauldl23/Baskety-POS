from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, F
from pos.models import Transaction, TransactionItem
from products.models import Product

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        from .models import UserSettings
        try:
            settings = self.request.user.settings
            if settings.default_landing_page != 'dashboard':
                # Map internal names to actual URL names
                landing_page_map = {
                    'pos': 'pos:index',
                    'inventory': 'inventory:dashboard',
                    'reports': 'reports:index',
                }
                url_name = landing_page_map.get(settings.default_landing_page, settings.default_landing_page)
                return reverse(url_name)
        except (UserSettings.DoesNotExist, AttributeError):
            pass
        return super().get_success_url()

@login_required
def dashboard(request):
    # Get today's date
    today = timezone.now().date()
    
    # Today's sales and transaction count (only completed transactions)
    today_transactions = Transaction.objects.filter(
        created_at__date=today,
        status='completed'
    )
    today_sales = today_transactions.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    transaction_count = today_transactions.count()
    
    # Low stock alerts - products below reorder level
    low_stock_count = Product.objects.filter(
        is_active=True,
        current_stock__lte=F('reorder_level')
    ).count()
    
    # Top product - most sold product (by quantity) from completed transactions
    top_product_data = TransactionItem.objects.filter(
        transaction__status='completed'
    ).values('product_name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold').first()
    
    top_product = top_product_data['product_name'] if top_product_data else 'N/A'
    
    context = {
        'today_sales': today_sales,
        'transaction_count': transaction_count,
        'low_stock_count': low_stock_count,
        'top_product': top_product,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        from .forms import UserProfileForm
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        from .forms import UserProfileForm
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def profile_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

@login_required
def settings_view(request):
    from .models import UserSettings
    from .forms import UserSettingsForm
    
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=settings)
    
    return render(request, 'accounts/settings.html', {
        'form': form,
    })
