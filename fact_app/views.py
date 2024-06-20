from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.

class HomeView(View):
    """Main View"""
    
    templates_name = 'index.html'
    
    """on utilise select_related par ce que on a des champs many to many cela 
    va facilité les requêtes.
    en fait ça fait ce qu'on appelle le sql any
    le any ça prend plusieurs tables reliés à une table 
    et le join pour en faire une seul table """
    
    invoices = Invoice.objects.select_related('customer', 'save_by').all()
    context = {
        'invoices': invoices
    }
    def get (self, request, *args, **kwargs):
        
        return render(request, self.templates_name, self.context)
    
    def post (self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)