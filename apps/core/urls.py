from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('deals/', views.DealsListView.as_view(), name='deals'),
    path('startups/', views.StartupsListView.as_view(), name='startups'),
    path('investors/', views.InvestorsListView.as_view(), name='investors'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('set-language/', views.set_language, name='set_language'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-deal/', views.CreateDealView.as_view(), name='create_deal'),
    path('create-startup/', views.CreateStartupView.as_view(), name='create_startup'),
    path('create-investor/', views.CreateInvestorView.as_view(), name='create_investor'),
] 