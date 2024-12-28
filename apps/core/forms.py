from django import forms
from django.utils.translation import gettext_lazy as _

class SignupForm(forms.Form):
    USER_TYPES = [
        ('investor', _('Investor')),
        ('startup', _('Startup')),
        ('individual', _('Individual')),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='investor'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Investor-specific fields
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    investment_range = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Startup-specific fields
    startup_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    industry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Individual-specific fields
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ) 