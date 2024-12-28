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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    company_name = models.CharField(max_length=255)
    investment_range_min = models.DecimalField(max_digits=15, decimal_places=2)
    investment_range_max = models.DecimalField(max_digits=15, decimal_places=2)
    sectors_of_interest = models.JSONField(default=list)
    investment_stage_preference = models.JSONField(default=list)
    total_investments_made = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Investor Profile')
        verbose_name_plural = _('Investor Profiles')

    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

class StartupProfile(models.Model):
    STAGES = [
        ('idea', _('Idea Stage')),
        ('mvp', _('MVP')),
        ('seed', _('Seed')),
        ('series_a', _('Series A')),
        ('series_b', _('Series B')),
        ('series_c', _('Series C')),
        ('growth', _('Growth')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='startup_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    stage = models.CharField(max_length=20, choices=STAGES)
    founding_date = models.DateField()
    website = models.URLField(blank=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    funding_target = models.DecimalField(max_digits=15, decimal_places=2)
    equity_offering = models.DecimalField(max_digits=5, decimal_places=2, help_text='Percentage')
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Startup Profile')
        verbose_name_plural = _('Startup Profiles')

    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

class IndividualProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='individual_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    linkedin_profile = models.URLField(blank=True)
    interests = models.JSONField(default=list)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Individual Profile')
        verbose_name_plural = _('Individual Profiles')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.email}" 