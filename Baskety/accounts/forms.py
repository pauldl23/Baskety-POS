from django import forms
from .models import User, UserSettings

class UserProfileForm(forms.ModelForm):
    # ... existing fields ...
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#4CAF50]/50 focus:border-[#4CAF50] transition-all font-medium text-gray-800',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#4CAF50]/50 focus:border-[#4CAF50] transition-all font-medium text-gray-800',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#4CAF50]/50 focus:border-[#4CAF50] transition-all font-medium text-gray-800',
                'placeholder': 'Email Address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#4CAF50]/50 focus:border-[#4CAF50] transition-all font-medium text-gray-800',
                'placeholder': 'Phone Number (Optional)'
            }),
        }

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['default_landing_page', 'theme_mode', 'compact_view', 'enable_notifications']
        widgets = {
            'default_landing_page': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#4CAF50]/50 focus:border-[#4CAF50] transition-all font-medium text-gray-800',
            }),
            'theme_mode': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#4CAF50]/50 focus:border-[#4CAF50] transition-all font-medium text-gray-800',
            }),
            'compact_view': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-[#4CAF50] border-gray-300 rounded focus:ring-[#4CAF50]',
            }),
            'enable_notifications': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-[#4CAF50] border-gray-300 rounded focus:ring-[#4CAF50]',
            }),
        }
