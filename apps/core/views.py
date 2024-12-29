from django.views.generic import TemplateView, FormView, CreateView
from django.utils import translation
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.conf import settings
from . import forms
from .forms import DealForm, StartupForm, InvestorForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'home.html'

class DealsListView(TemplateView):
    template_name = 'core/deals_list.html'

class StartupsListView(TemplateView):
    template_name = 'core/startups_list.html'

class InvestorsListView(TemplateView):
    template_name = 'core/investors_list.html' 

def set_language(request):
    lang = request.GET.get('lang', 'en')
    if lang in [code for code, name in settings.LANGUAGES]:
        translation.activate(lang)
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
    return redirect('/') 

class SignupView(FormView):
    template_name = 'core/signup.html'
    form_class = forms.SignupForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        # Handle form submission here
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.request.GET.get('type', 'investor')
        context['user_type'] = user_type
        return context 

@login_required(login_url='admin:login')
def dashboard(request):
    # Get all companies associated with the user
    user_companies = []
    
    # Check for startups
    try:
        if hasattr(request.user, 'startup'):
            user_companies.append({
                'name': request.user.startup.company_name,
                'type': 'startup',
                'id': request.user.startup.id
            })
    except:
        pass
    
    # Check for investment firms
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
    template_name = 'core/create_deal.html'
    login_url = 'admin:login'
    form_class = DealForm
    
    def get_success_url(self):
        return reverse_lazy('core:dashboard')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Deal created successfully!')
        return super().form_valid(form)

class CreateStartupView(LoginRequiredMixin, CreateView):
    template_name = 'core/create_startup.html'
    login_url = 'admin:login'
    form_class = StartupForm
    
    def get_success_url(self):
        return reverse_lazy('core:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Startup registered successfully!')
        return super().form_valid(form)

class CreateInvestorView(LoginRequiredMixin, CreateView):
    template_name = 'core/create_investor.html'
    login_url = 'admin:login'
    form_class = InvestorForm
    
    def get_success_url(self):
        return reverse_lazy('core:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Investment firm registered successfully!')
        return super().form_valid(form) 