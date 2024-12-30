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
from .models import Deal, StartupProfile, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class HomeView(TemplateView):
    """Landing page view for the application.
    
    Displays the main homepage with featured content and navigation options.
    Inherits from Django's TemplateView for simple template rendering.
    """
    template_name: str = 'home.html'


class DealsListView(ListView):
    """View for displaying a paginated list of active investment deals.
    
    Displays investment opportunities in a grid layout with pagination.
    Only shows active deals and orders them by creation date.
    
    Attributes:
        template_name (str): Path to the template file
        model (type): The Deal model class
        context_object_name (str): Name of the deals list in template context
        paginate_by (int): Number of deals to display per page
        ordering (list): Field(s) to order the deals by
    """
    template_name: str = 'core/deals_list.html'
    model = Deal
    context_object_name: str = 'deals'
    paginate_by: int = 9  # Show 9 deals per page (3x3 grid)
    ordering: list[str] = ['-created_at']  # Show newest deals first

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
        return context


class StartupsListView(ListView):
    """View for displaying a paginated list of verified startups.
    
    Displays startup profiles in a grid layout with pagination.
    Only shows verified startups and orders them by founding date.
    
    Attributes:
        template_name (str): Path to the template file
        model (type): The StartupProfile model class
        context_object_name (str): Name of the startups list in template context
        paginate_by (int): Number of startups to display per page
        ordering (list): Field(s) to order the startups by
    """
    template_name: str = 'core/startups_list.html'
    model = StartupProfile
    context_object_name: str = 'startups'
    paginate_by: int = 9  # Show 9 startups per page (3x3 grid)
    ordering: list[str] = ['-founding_date']  # Show newest startups first

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
        return context


class InvestorsListView(TemplateView):
    """View for displaying a list of investors.
    
    Displays investor profiles and their investment preferences.
    
    Attributes:
        template_name (str): Path to the template file
    """
    template_name: str = 'core/investors_list.html'


def set_language(request: HttpRequest) -> HttpResponse:
    """Handle language switching for internationalization.
    
    Sets the user's preferred language and redirects back to the previous page.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Redirect response to the previous page or home
    """
    lang = request.GET.get('lang', 'en')
    if lang in [code for code, name in settings.LANGUAGES]:
        translation.activate(lang)
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
    return redirect('/')


class SignupView(FormView):
    """View for handling user registration.
    
    Manages the signup process for new users with different account types
    (investor, startup, individual).
    
    Attributes:
        template_name (str): Path to the template file
        form_class (type): The form class for user registration
        success_url (str): URL to redirect to after successful registration
    """
    template_name: str = 'core/signup.html'
    form_class = forms.SignupForm
    success_url: str = reverse_lazy('core:home')

    def form_valid(self, form: forms.SignupForm) -> HttpResponse:
        """Process the valid form submission.
        
        Args:
            form (SignupForm): The validated form instance
            
        Returns:
            HttpResponse: Redirect response after successful registration
        """
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Enhance the template context with user type information.
        
        Args:
            **kwargs: Additional keyword arguments from the parent class
            
        Returns:
            Dict[str, Any]: The enhanced template context
        """
        context = super().get_context_data(**kwargs)
        user_type = self.request.GET.get('type', 'investor')
        context['user_type'] = user_type
        return context


@login_required(login_url='admin:login')
def dashboard(request: HttpRequest) -> HttpResponse:
    """View for user dashboard displaying associated companies.
    
    Shows companies (startups/investment firms) associated with the logged-in user.
    
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
        'user_companies': user_companies
    }
    
    return render(request, 'core/dashboard.html', context)


class CreateDealView(LoginRequiredMixin, CreateView):
    """View for creating new investment deals.
    
    Handles the creation of new deals by startups seeking investment.
    Requires user authentication.
    
    Attributes:
        template_name (str): Path to the template file
        login_url (str): URL to redirect to if user is not authenticated
        form_class (type): The form class for deal creation
    """
    template_name: str = 'core/create_deal.html'
    login_url: str = 'admin:login'
    form_class = DealForm
    
    def get_success_url(self) -> str:
        """Get the URL to redirect to after successful deal creation.
        
        Returns:
            str: URL for redirection after success
        """
        return reverse_lazy('core:dashboard')

    def form_valid(self, form: DealForm) -> HttpResponse:
        """Process the valid form submission.
        
        Sets the creator of the deal to the current user and displays success message.
        
        Args:
            form (DealForm): The validated form instance
            
        Returns:
            HttpResponse: Redirect response after successful deal creation
        """
        form.instance.creator = self.request.user
        messages.success(self.request, 'Deal created successfully!')
        return super().form_valid(form)


class CreateStartupView(LoginRequiredMixin, CreateView):
    """View for creating new startup profiles.
    
    Handles the creation of startup profiles by entrepreneurs.
    Requires user authentication.
    
    Attributes:
        template_name (str): Path to the template file
        login_url (str): URL to redirect to if user is not authenticated
        form_class (type): The form class for startup profile creation
    """
    template_name: str = 'core/create_startup.html'
    login_url: str = 'admin:login'
    form_class = StartupForm
    
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
        messages.success(self.request, 'Startup registered successfully!')
        return super().form_valid(form)


class CreateInvestorView(LoginRequiredMixin, CreateView):
    """View for creating new investor profiles.
    
    Handles the creation of investor profiles by investment firms or individuals.
    Requires user authentication.
    
    Attributes:
        template_name (str): Path to the template file
        login_url (str): URL to redirect to if user is not authenticated
        form_class (type): The form class for investor profile creation
    """
    template_name: str = 'core/create_investor.html'
    login_url: str = 'admin:login'
    form_class = InvestorForm
    
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
        messages.success(self.request, 'Investment firm registered successfully!')
        return super().form_valid(form) 