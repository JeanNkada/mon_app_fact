from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

# Create your views here.

class HomeView(View):
    """Main View"""
    
    templates_name = 'index.html'
    
    """on utilise select_related par ce qu'on a des champs many to many cela 
    va facilité les requêtes.
    en fait ça fait ce qu'on appelle le sql any
    le any prend plusieurs tables reliés à une table 
    et les joins pour en faire une seul table """
    
    invoices = Invoice.objects.select_related('customer', 'save_by').all()
    context = {
        'invoices': invoices
    }
    def get(self, request, *args, **kwargs):
        
        return render(request, self.templates_name, self.context)
    
    def post(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)
    
# dedut du coded'enregistrement d'un nouveau client
class AddCustomerView(View):
    """Add new customer"""
    templates_name = 'add_customer.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name)

    def post(self, request, *args, **kwargs):
        data ={
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'sex': request.POST.get('sex'),
            'zip_code': request.POST.get('zip_code'),
            'save_by': request.user
                }
        try:
            created = Customer.objects.create(**data)
            if created:
                messages.success(request, 'Customer registered successfully.')
            else:
                messages.error(request, 'Sorry, pleace try again the sent data is corrupt.')
                
        except Exception as e:
            messages.error(request, f'Sorry our system is detecting the following issues {e}')
            
        return render(request, self.templates_name)
# fin d'enrégistrement du nouveau client