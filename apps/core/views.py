from django.views.generic import TemplateView
from django.utils import translation
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

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