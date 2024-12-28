from django.views.generic import TemplateView, FormView
from django.utils import translation
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from . import forms

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