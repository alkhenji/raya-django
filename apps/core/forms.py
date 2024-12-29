from django import forms
from .models import IndividualProfile, InvestorProfile, StartupProfile, Deal, User

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'user_type']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

class IndividualForm(forms.ModelForm):
    class Meta:
        model = IndividualProfile
        fields = ['first_name', 'last_name', 'title', 'company', 'interests', 'linkedin_url']

class InvestorForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        fields = [
            'company_name', 'description', 'website', 'location', 'founded_year', 'team_size',
            'preferred_industries', 'preferred_stages', 'investment_range_min', 'investment_range_max',
            'sectors_of_interest', 'linkedin_url', 'crunchbase_url'
        ]

class StartupForm(forms.ModelForm):
    class Meta:
        model = StartupProfile
        fields = [
            'company_name', 'tagline', 'description', 'industry', 'stage', 'founding_date',
            'location', 'team_size', 'revenue_range', 'website', 'linkedin_url', 'crunchbase_url',
            'pitch_deck', 'current_funding_target', 'min_ticket_size', 'equity_offering'
        ]

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = [
            'title', 'description', 'deal_type', 'amount', 'equity_offered',
            'min_investment', 'target_close_date', 'industry', 'deal_documents',
            'terms_and_conditions'
        ]
        widgets = {
            'target_close_date': forms.DateInput(attrs={'type': 'date'}),
        } 