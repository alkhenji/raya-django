from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPES = [
        ('investor', _('Investor')),
        ('startup', _('Startup')),
        ('individual', _('Individual')),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='individual'
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class InvestorProfile(models.Model):
    INVESTMENT_STAGES = [
        ('seed', _('Seed')),
        ('series_a', _('Series A')),
        ('series_b', _('Series B')),
        ('series_c', _('Series C')),
        ('growth', _('Growth')),
        ('any', _('Any Stage')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255)
    founded_year = models.PositiveIntegerField()
    team_size = models.PositiveIntegerField()
    
    # Investment preferences
    preferred_industries = models.JSONField(default=list, blank=True)
    preferred_stages = models.JSONField(default=list, choices=INVESTMENT_STAGES)
    investment_range_min = models.DecimalField(max_digits=15, decimal_places=2)
    investment_range_max = models.DecimalField(max_digits=15, decimal_places=2)
    sectors_of_interest = models.JSONField(default=list)
    
    # Portfolio
    total_investments = models.PositiveIntegerField(default=0)
    portfolio_companies = models.ManyToManyField('StartupProfile', related_name='investors', blank=True)
    total_capital_deployed = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Verification
    verified = models.BooleanField(default=False)
    linkedin_url = models.URLField(blank=True)
    crunchbase_url = models.URLField(blank=True)

    class Meta:
        verbose_name = _('Investor Profile')
        verbose_name_plural = _('Investor Profiles')

    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

class StartupProfile(models.Model):
    STAGES = [
        ('idea', _('مرحلة الفكرة')),
        ('mvp', _('النموذج الأولي')),
        ('seed', _('مرحلة التأسيس')),
        ('series_a', _('الجولة الأولى')),
        ('series_b', _('الجولة الثانية')),
        ('series_c', _('الجولة الثالثة')),
        ('growth', _('مرحلة النمو')),
    ]

    REVENUE_RANGES = [
        ('pre_revenue', _('ما قبل الإيرادات')),
        ('0-100k', _('0 - 100 ألف دولار')),
        ('100k-500k', _('100 - 500 ألف دولار')),
        ('500k-1m', _('500 ألف - مليون دولار')),
        ('1m-5m', _('مليون - 5 مليون دولار')),
        ('5m+', _('أكثر من 5 مليون دولار')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='startup_profile')
    company_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    
    # Company Details
    industry = models.CharField(max_length=100)
    stage = models.CharField(max_length=20, choices=STAGES)
    founding_date = models.DateField()
    location = models.CharField(max_length=255)
    team_size = models.PositiveIntegerField()
    revenue_range = models.CharField(max_length=20, choices=REVENUE_RANGES, default='pre_revenue')
    
    # Online Presence
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    crunchbase_url = models.URLField(blank=True)
    
    # Fundraising
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    total_funding_raised = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_funding_target = models.DecimalField(max_digits=15, decimal_places=2)
    min_ticket_size = models.DecimalField(max_digits=15, decimal_places=2)
    equity_offering = models.DecimalField(max_digits=5, decimal_places=2, help_text='Percentage')
    
    # Metrics
    key_metrics = models.JSONField(default=dict, blank=True, help_text='Key performance metrics')
    
    # Verification
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Startup Profile')
        verbose_name_plural = _('Startup Profiles')

    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

class Deal(models.Model):
    DEAL_STATUS = [
        ('draft', _('Draft')),
        ('active', _('Active')),
        ('in_discussion', _('In Discussion')),
        ('due_diligence', _('Due Diligence')),
        ('closed', _('Closed')),
        ('cancelled', _('Cancelled')),
    ]

    DEAL_TYPE = [
        ('equity', _('Equity')),
        ('convertible_note', _('Convertible Note')),
        ('safe', _('SAFE')),
        ('debt', _('Debt')),
        ('other', _('Other')),
    ]

    # Basic Deal Info
    title = models.CharField(max_length=200)
    description = models.TextField()
    startup = models.ForeignKey(StartupProfile, on_delete=models.CASCADE, related_name='deals')
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE, default='equity')
    status = models.CharField(max_length=20, choices=DEAL_STATUS, default='draft')
    
    # Deal Terms
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    equity_offered = models.DecimalField(max_digits=5, decimal_places=2, help_text='Percentage')
    min_investment = models.DecimalField(max_digits=15, decimal_places=2)
    target_close_date = models.DateField()
    
    # Deal Progress
    amount_raised = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    number_of_investors = models.PositiveIntegerField(default=0)
    interested_investors = models.ManyToManyField(InvestorProfile, related_name='interested_deals', blank=True)
    committed_investors = models.ManyToManyField(InvestorProfile, related_name='committed_deals', blank=True)
    
    # Additional Info
    industry = models.CharField(max_length=100)
    deal_documents = models.FileField(upload_to='deal_documents/', blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.startup.company_name}"

class IndividualProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='individual_profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    interests = models.JSONField(default=list, blank=True)
    linkedin_url = models.URLField(blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Individual Profile')
        verbose_name_plural = _('Individual Profiles')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.email}" 