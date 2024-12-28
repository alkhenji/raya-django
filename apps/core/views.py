from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class DealsListView(TemplateView):
    template_name = 'core/deals_list.html'

class StartupsListView(TemplateView):
    template_name = 'core/startups_list.html'

class InvestorsListView(TemplateView):
    template_name = 'core/investors_list.html' 