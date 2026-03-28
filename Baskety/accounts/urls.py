from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, dashboard, profile_view, profile_edit_view, profile_password_view, settings_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('profile/password/', profile_password_view, name='change_password'),
    path('settings/', settings_view, name='settings'),
    path('', CustomLoginView.as_view(), name='home'), # Redirect root to login
]
