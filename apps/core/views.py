from django.views.generic import TemplateView, FormView, CreateView, ListView
from django.utils import translation
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from typing import Any, Dict, Optional
from . import forms
from .forms import DealForm, StartupForm, InvestorForm
from .models import Deal, StartupProfile, User, InvestorProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from django.utils.translation import get_language
from django.db import IntegrityError


class HomeView(TemplateView):
    """Landing page view for the application.
    
    Shows different content based on user type and language:
    - Admins see the admin dashboard
    - Non-admins see the public landing page with platform features
    - Arabic users see the RTL version with Arabic content
    """
    
    def get_template_names(self) -> list[str]:
        """Return different templates based on user type and language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ['home_admin.html']
        
        # Use Arabic template if language is Arabic
        if translation.get_language() == 'ar':
            return ['home_ar.html']
        return ['home.html']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with statistics and features.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        
        # Only add these stats for non-admin view
        if not (self.request.user.is_authenticated and self.request.user.is_staff):
            is_arabic = translation.get_language() == 'ar'
            
            features = [
                {
                    'icon': 'fas fa-handshake',
                    'title': _('تواصل') if is_arabic else _('Connect'),
                    'description': _('تواصل مباشرة مع المستثمرين المعتمدين والشركات الناشئة الواعدة.') if is_arabic else _('Connect directly with verified investors and promising startups.')
                },
                {
                    'icon': 'fas fa-chart-line',
                    'title': _('نمو') if is_arabic else _('Grow'),
                    'description': _('احصل على رأس المال اللازم للنمو والشراكات الاستراتيجية.') if is_arabic else _('Access growth capital and strategic partnerships.')
                },
                {
                    'icon': 'fas fa-search-dollar',
                    'title': _('اكتشف') if is_arabic else _('Discover'),
                    'description': _('اعثر على فرص استثمارية تتناسب مع معاييرك.') if is_arabic else _('Find investment opportunities that match your criteria.')
                },
                {
                    'icon': 'fas fa-shield-alt',
                    'title': _('ثقة') if is_arabic else _('Trust'),
                    'description': _('ملفات شخصية موثقة وإدارة آمنة للصفقات.') if is_arabic else _('Verified profiles and secure deal management.')
                },
            ]
            
            context.update({
                'stats': {
                    'startups': StartupProfile.objects.filter(verified=True).count(),
                    'investors': InvestorProfile.objects.filter(verified=True).count(),
                    'deals': Deal.objects.filter(status='active').count(),
                    'total_investment': Deal.objects.filter(status='closed').aggregate(
                        total=models.Sum('amount_raised')
                    )['total'] or 0,
                },
                'features': features,
                'recent_deals': Deal.objects.filter(
                    status='active'
                ).select_related('startup').order_by('-created_at')[:3],
                'featured_startups': StartupProfile.objects.filter(
                    verified=True
                ).order_by('-total_funding_raised')[:3],
                'top_investors': InvestorProfile.objects.filter(
                    verified=True
                ).order_by('-total_investments')[:3],
            })
            
            # Add language switcher context
            context['languages'] = settings.LANGUAGES
            context['current_language'] = translation.get_language()
        
        return context


class DealsListView(ListView):
    """View for displaying a paginated list of active investment deals.
    
    Displays investment opportunities in a grid layout with pagination.
    Only shows active deals and orders them by creation date.
    Supports both English and Arabic interfaces.
    
    Attributes:
        model (type): The Deal model class
        context_object_name (str): Name of the deals list in template context
        paginate_by (int): Number of deals to display per page
        ordering (list): Field(s) to order the deals by
    """
    model = Deal
    context_object_name: str = 'deals'
    paginate_by: int = 9  # Show 9 deals per page (3x3 grid)
    ordering: list[str] = ['-created_at']  # Show newest deals first

    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/deals_list_ar.html']
        return ['core/deals_list.html']

    def get_queryset(self) -> QuerySet[Deal]:
        """Filter and return the queryset of deals.
        
        Returns:
            QuerySet[Deal]: Filtered queryset containing only active deals
        """
        queryset = super().get_queryset()
        return queryset.filter(status='active')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with additional data.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        context.update({
            'current_language': translation.get_language(),
            'languages': settings.LANGUAGES,
            'can_create_deal': self.request.user.is_authenticated
        })
        return context


class StartupsListView(ListView):
    """View for displaying a paginated list of verified startups.
    
    Displays startup profiles in a grid layout with pagination.
    Only shows verified startups and orders them by founding date.
    Supports both English and Arabic interfaces.
    
    Attributes:
        model (type): The StartupProfile model class
        context_object_name (str): Name of the startups list in template context
        paginate_by (int): Number of startups to display per page
        ordering (list): Field(s) to order the startups by
    """
    model = StartupProfile
    context_object_name: str = 'startups'
    paginate_by: int = 9  # Show 9 startups per page (3x3 grid)
    ordering: list[str] = ['-founding_date']  # Show newest startups first

    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/startups_list_ar.html']
        return ['core/startups_list.html']

    def get_queryset(self) -> QuerySet[StartupProfile]:
        """Filter and return the queryset of startups.
        
        Returns:
            QuerySet[StartupProfile]: Filtered queryset containing only verified startups
        """
        queryset = super().get_queryset()
        return queryset.filter(verified=True)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with additional data.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        context['current_language'] = translation.get_language()
        context['languages'] = settings.LANGUAGES
        return context


class InvestorsListView(ListView):
    """View for displaying a paginated list of verified investors.
    
    Displays investor profiles and their investment preferences in a grid layout.
    Only shows verified investors and orders them by total investments.
    Supports both English and Arabic interfaces.
    
    Attributes:
        model (type): The InvestorProfile model class
        context_object_name (str): Name of the investors list in template context
        paginate_by (int): Number of investors to display per page
        ordering (list): Field(s) to order the investors by
    """
    model = InvestorProfile
    context_object_name: str = 'investors'
    paginate_by: int = 9  # Show 9 investors per page (3x3 grid)
    ordering: list[str] = ['-total_investments']  # Show most active investors first

    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/investors_list_ar.html']
        return ['core/investors_list.html']

    def get_queryset(self) -> QuerySet[InvestorProfile]:
        """Filter and return the queryset of investors.
        
        Returns:
            QuerySet[InvestorProfile]: Filtered queryset containing only verified investors
        """
        queryset = super().get_queryset()
        return queryset.filter(verified=True)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with additional data.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        context['current_language'] = translation.get_language()
        context['languages'] = settings.LANGUAGES
        return context


def set_language(request: HttpRequest) -> HttpResponse:
    """Handle language switching for internationalization.
    
    Sets the user's preferred language and redirects back to the previous page.
    Supports switching between English and Arabic interfaces.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Redirect response to the previous page or home
    """
    lang = request.GET.get('lang', settings.LANGUAGE_CODE)
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    
    if lang in dict(settings.LANGUAGES):
        if next_url == '/':
            next_url = '/{}/'.format(lang)
            
        translation.activate(lang)
        response = redirect(next_url)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, 
            lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE or None,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response
        
    return redirect('/')


class SignupView(FormView):
    """View for handling user registration.
    
    Manages the signup process for new users with different account types
    (investor, startup, individual). Supports both English and Arabic interfaces.
    
    Attributes:
        form_class (type): The form class for user registration
        success_url (str): URL to redirect to after successful registration
    """
    form_class = forms.SignupForm
    success_url: str = reverse_lazy('core:dashboard')

    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/signup_ar.html']
        return ['core/signup.html']

    def form_valid(self, form: forms.SignupForm) -> HttpResponse:
        """Process the valid form submission.
        
        Args:
            form (SignupForm): The validated form instance
            
        Returns:
            HttpResponse: Redirect response after successful registration
        """
        user = form.save(commit=False)
        user.user_type = self.request.GET.get('type', 'investor')
        # Use full email as username
        user.username = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        
        # Log the user in
        from django.contrib.auth import login
        login(self.request, user)
        
        messages.success(
            self.request,
            _('تم إنشاء حسابك بنجاح!') if translation.get_language() == 'ar' else _('Your account has been created successfully!')
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with user type and language information.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        user_type = self.request.GET.get('type', 'investor')
        context.update({
            'user_type': user_type,
            'current_language': translation.get_language(),
            'languages': settings.LANGUAGES
        })
        return context


@login_required(login_url='admin:login')
def dashboard(request: HttpRequest) -> HttpResponse:
    """View for user dashboard displaying associated companies.
    
    Shows companies (startups/investment firms) associated with the logged-in user.
    Supports both English and Arabic interfaces.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered dashboard template with context
    """
    user_companies: list[dict] = []
    
    try:
        if hasattr(request.user, 'startup'):
            user_companies.append({
                'name': request.user.startup.company_name,
                'type': 'startup',
                'id': request.user.startup.id
            })
    except:
        pass
    
    try:
        if hasattr(request.user, 'investor'):
            user_companies.append({
                'name': request.user.investor.company_name,
                'type': 'investor',
                'id': request.user.investor.id
            })
    except:
        pass
    
    context = {
        'user_companies': user_companies,
        'current_language': translation.get_language(),
        'languages': settings.LANGUAGES
    }
    
    template_name = 'core/dashboard_ar.html' if translation.get_language() == 'ar' else 'core/dashboard.html'
    return render(request, template_name, context)


class CreateDealView(LoginRequiredMixin, CreateView):
    """View for creating new investment deals.
    
    Handles the creation of new deals by startups seeking investment.
    Requires user authentication. Supports both English and Arabic interfaces.
    
    Attributes:
        login_url (str): URL to redirect to if user is not authenticated
        form_class (type): The form class for deal creation
    """
    login_url: str = 'core:signup'
    form_class = DealForm
    
    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/create_deal_ar.html']
        return ['core/create_deal.html']

    def get_success_url(self) -> str:
        """Get the URL to redirect to after successful deal creation.
        
        Returns:
            str: URL for redirection after success
        """
        return reverse_lazy('core:deals_list')

    def form_valid(self, form: DealForm) -> HttpResponse:
        """Process the valid form submission.
        
        Sets the creator of the deal to the current user and displays success message.
        
        Args:
            form (DealForm): The validated form instance
            
        Returns:
            HttpResponse: Redirect response after successful deal creation
        """
        form.instance.creator = self.request.user
        try:
            form.instance.startup = self.request.user.startup
        except StartupProfile.DoesNotExist:
            messages.error(
                self.request,
                _('يجب عليك إنشاء ملف شركتك الناشئة أولاً.') if translation.get_language() == 'ar' else _('You need to create your startup profile first.')
            )
            return redirect('core:create_startup')
            
        messages.success(
            self.request, 
            _('تم إنشاء الفرصة الاستثمارية بنجاح!') if translation.get_language() == 'ar' else _('Deal created successfully!')
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with language information.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        context['current_language'] = translation.get_language()
        context['languages'] = settings.LANGUAGES
        return context


class CreateStartupView(LoginRequiredMixin, CreateView):
    """View for creating new startup profiles.
    
    Handles the creation of startup profiles by entrepreneurs.
    Requires user authentication. Supports both English and Arabic interfaces.
    
    Attributes:
        login_url (str): URL to redirect to if user is not authenticated
        form_class (type): The form class for startup profile creation
    """
    form_class = StartupForm
    
    def get_login_url(self) -> str:
        """Get the URL to redirect to when user is not authenticated.
        
        Returns:
            str: URL for redirection with type parameter
        """
        return reverse_lazy('core:signup') + '?type=startup'

    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/create_startup_ar.html']
        return ['core/create_startup.html']

    def get_success_url(self) -> str:
        """Get the URL to redirect to after successful profile creation.
        
        Returns:
            str: URL for redirection after success
        """
        return reverse_lazy('core:dashboard')

    def form_valid(self, form: StartupForm) -> HttpResponse:
        """Process the valid form submission.
        
        Sets the user of the startup profile to the current user and displays success message.
        
        Args:
            form (StartupForm): The validated form instance
            
        Returns:
            HttpResponse: Redirect response after successful profile creation
        """
        form.instance.user = self.request.user
        messages.success(
            self.request, 
            _('تم تسجيل الشركة الناشئة بنجاح!') if translation.get_language() == 'ar' else _('Startup registered successfully!')
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with language information.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        context['current_language'] = translation.get_language()
        context['languages'] = settings.LANGUAGES
        return context


class CreateInvestorView(LoginRequiredMixin, CreateView):
    """View for creating new investor profiles.
    
    Handles the creation of investor profiles by investment firms or individuals.
    Requires user authentication. Supports both English and Arabic interfaces.
    
    Attributes:
        login_url (str): URL to redirect to if user is not authenticated
        form_class (type): The form class for investor profile creation
    """
    form_class = InvestorForm
    
    def get_login_url(self) -> str:
        """Get the URL to redirect to when user is not authenticated.
        
        Returns:
            str: URL for redirection with type parameter
        """
        return reverse_lazy('core:signup') + '?type=investor'

    def get_template_names(self) -> list[str]:
        """Return different templates based on language.
        
        Returns:
            list[str]: List containing the appropriate template name
        """
        if translation.get_language() == 'ar':
            return ['core/create_investor_ar.html']
        return ['core/create_investor.html']

    def get_success_url(self) -> str:
        """Get the URL to redirect to after successful profile creation.
        
        Returns:
            str: URL for redirection after success
        """
        return reverse_lazy('core:dashboard')

    def form_valid(self, form: InvestorForm) -> HttpResponse:
        """Process the valid form submission.
        
        Sets the user of the investor profile to the current user and displays success message.
        
        Args:
            form (InvestorForm): The validated form instance
            
        Returns:
            HttpResponse: Redirect response after successful profile creation
        """
        form.instance.user = self.request.user
        messages.success(
            self.request, 
            _('تم تسجيل المستثمر بنجاح!') if translation.get_language() == 'ar' else _('Investment firm registered successfully!')
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with language information.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        context['current_language'] = translation.get_language()
        context['languages'] = settings.LANGUAGES
        return context 


class LoginView(auth_views.LoginView):
    """
    Custom login view that extends Django's built-in LoginView.
    Handles user authentication and provides language-specific templates.
    """
    def get_template_names(self):
        """Return the appropriate template based on the current language."""
        if get_language() == 'ar':
            return ['core/login_ar.html']
        return ['core/login.html'] 