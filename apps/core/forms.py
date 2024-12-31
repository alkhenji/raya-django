from django import forms
from django.utils.translation import gettext_lazy as _
from .models import IndividualProfile, InvestorProfile, StartupProfile, Deal, User

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        help_text=_('Enter a strong password with at least 8 characters')
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password again for verification')
    )

    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email': _('Email'),
        }
        help_texts = {
            'email': _('We will use this email to contact you'),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The two password fields did not match'))
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
        labels = {
            'company_name': _('اسم الشركة'),
            'tagline': _('الشعار'),
            'description': _('الوصف'),
            'industry': _('المجال'),
            'stage': _('المرحلة'),
            'founding_date': _('تاريخ التأسيس'),
            'location': _('الموقع'),
            'team_size': _('حجم الفريق'),
            'revenue_range': _('نطاق الإيرادات'),
            'website': _('الموقع الإلكتروني'),
            'linkedin_url': _('رابط LinkedIn'),
            'crunchbase_url': _('رابط Crunchbase'),
            'pitch_deck': _('عرض الشركة'),
            'current_funding_target': _('هدف التمويل الحالي'),
            'min_ticket_size': _('الحد الأدنى للاستثمار'),
            'equity_offering': _('نسبة الأسهم المعروضة')
        }
        help_texts = {
            'company_name': _('اسم شركتك الناشئة كما هو مسجل رسمياً'),
            'tagline': _('وصف موجز لشركتك في جملة واحدة'),
            'description': _('وصف تفصيلي لشركتك ومنتجاتها وخدماتها'),
            'industry': _('المجال الرئيسي لعمل الشركة'),
            'stage': _('المرحلة الحالية للشركة'),
            'founding_date': _('تاريخ تأسيس الشركة'),
            'location': _('المدينة والدولة التي تعمل فيها الشركة'),
            'team_size': _('عدد أعضاء الفريق بدوام كامل'),
            'revenue_range': _('نطاق الإيرادات السنوية الحالية'),
            'website': _('رابط الموقع الإلكتروني للشركة'),
            'linkedin_url': _('رابط صفحة الشركة على LinkedIn'),
            'crunchbase_url': _('رابط صفحة الشركة على Crunchbase'),
            'pitch_deck': _('عرض تقديمي عن الشركة (PDF)'),
            'current_funding_target': _('مبلغ التمويل المستهدف بالدولار الأمريكي'),
            'min_ticket_size': _('الحد الأدنى للاستثمار المقبول بالدولار الأمريكي'),
            'equity_offering': _('نسبة الأسهم المعروضة مقابل الاستثمار')
        }
        widgets = {
            'founding_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'pitch_deck': forms.FileInput(attrs={'accept': '.pdf'})
        }

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