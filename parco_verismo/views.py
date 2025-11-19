from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'parco_verismo/index.html'

class EventiView(TemplateView):
    template_name = 'parco_verismo/eventi.html'

class NewsView(TemplateView):
    template_name = 'parco_verismo/news.html'
