from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, InvestorProfile, StartupProfile, IndividualProfile, Deal

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'user_type', 'bio', 'profile_image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'location', 'total_investments', 'total_capital_deployed', 'verified')
    list_filter = ('verified', 'location')
    search_fields = ('company_name', 'user__email', 'location')

@admin.register(StartupProfile)
class StartupProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'stage', 'location', 'revenue_range', 'verified')
    list_filter = ('stage', 'verified', 'industry', 'revenue_range', 'location')
    search_fields = ('company_name', 'user__email', 'industry', 'location')

@admin.register(IndividualProfile)
class IndividualProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user', 'title', 'company', 'verified')
    list_filter = ('verified',)
    search_fields = ('first_name', 'last_name', 'user__email', 'company')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = _('Full Name')

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'startup', 'deal_type', 'amount', 'status', 'created_at')
    list_filter = ('status', 'deal_type', 'created_at')
    search_fields = ('title', 'startup__company_name', 'industry')
    readonly_fields = ('amount_raised', 'number_of_investors', 'created_at', 'updated_at') 