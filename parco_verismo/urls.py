from django.urls import path
from . import views

app_name = 'parco_verismo'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('eventi/', views.EventiView.as_view(), name='eventi'),
    path('news/', views.NewsView.as_view(), name='news'),
]
