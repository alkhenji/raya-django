from django.urls import path
from . import views

app_name = 'core'

from .views import (
    HomeView, DealsListView, StartupsListView, InvestorsListView,
    CreateDealView, CreateStartupView, CreateInvestorView,
    SignupView, LoginView, set_language, dashboard
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('set-language/', set_language, name='set_language'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('deals/', DealsListView.as_view(), name='deals_list'),
    path('startups/', StartupsListView.as_view(), name='startups_list'),
    path('investors/', InvestorsListView.as_view(), name='investors_list'),
    path('deals/create/', CreateDealView.as_view(), name='create_deal'),
    path('startups/create/', CreateStartupView.as_view(), name='create_startup'),
    path('investors/create/', CreateInvestorView.as_view(), name='create_investor'),
] 