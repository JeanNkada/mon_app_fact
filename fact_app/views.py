from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

from django.http import HttpResponse

import pdfkit

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .decorators import *

import os

from django.template.loader import get_template

from django.db import transaction

from .utils import pagination, get_invoice




# code pour lister les factures sur l'ecran
class HomeView(LoginRequiredSuperuserMixin, View):
    """Main View"""
    
    templates_name = 'index.html'
    
    """on utilise select_related par ce qu'on a des champs many to many cela 
    va facilité les requêtes.
    en fait ça fait ce qu'on appelle le sql any
    le any prend plusieurs tables reliés à une table 
    et les joins pour en faire une seul table """
    
    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')
    
    context = {
        'invoices': invoices
    }
    
    def get(self, request, *args, **kwargs):
        
        items = pagination(request, self.invoices)
        
        self.context['invoices'] = items
        
        return render(request, self.templates_name, self.context)
    
    def post(self, request, *args, **kwargs):
        
        #modify
        if request.POST.get('id_modified'):
            
            paid = request.POST.get('modified')
            
            try:
                obj =Invoice.objects.get(id=request.POST.get('id_modified'))
                
                if paid == 'True':
                    
                    obj.paid = True
                    
                else:
                    
                    obj.paid = False
                    
                obj.save()
                
                messages.success(request, 'Invoice status updated successfully.')
                
            except Exception as e:
                
                messages.error(request, f'Error updating invoice status: {e}')
            
        #delete
        if request.POST.get('id_delete'):
            
            try:
                obj = Invoice.objects.get(id=request.POST.get('id_delete'))
                
                obj.delete()
                
                messages.success(request, 'Invoice deleted successfully.')
                
            except Exception as e:
                
                messages.error(request, f'Error deleting invoice: {e}')
            
        # pagination
        if request.POST.get('page'):
            
            page = request.POST.get('page')
            
            items = pagination(request, self.invoices, page)
            
            self.context['invoices'] = items
            
        return render(request, self.templates_name, self.context)
            
    
# dedut du coded'enregistrement d'un nouveau client
class AddCustomerView(LoginRequiredSuperuserMixin, View):
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

# dedut du code d'enregistrement d'une nouvelle facture
class AddInvoiceView(LoginRequiredSuperuserMixin, View):
    
    """Add new invoice view"""
    
    templates_name = 'add_invoice.html'
    customers = Customer.objects.select_related('save_by').all()
    context = {
        'customers': customers 
    }
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.templates_name, self.context)
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        
        items = []
        
        try:
            
            customer = request.POST.get('customer')
            
            type =request.POST.get('invoice_type')
            
            articles = request.POST.getlist('article') # getlist pour la recupération de tous les articles
            
            qties = request.POST.getlist('qty')
            
            units = request.POST.getlist('unit')
            
            total_a = request.POST.getlist('total-a')
            
            total = request.POST.get('total')
            
            comment = request.POST.get('comment')
            
            # creaton de l'objet facture
            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,
                'total': total,
                'invoice_type': type,
                'comment': comment
            }
            
            invoice = Invoice.objects.create(**invoice_object)
            
            # maintenant on lie les objets aux articles
            for index, article in enumerate(articles):
                
                data = Article(
                    invoice_id= invoice.id,
                    name = article,
                    quantity = qties[index],
                    unit_price = units[index],
                    total = total_a[index],
                )
                
                items.append(data)
            
            created = Article.objects.bulk_create(items)# prend un ensemble d'object et crait une fois
            
            if created:
                messages.success(request, 'Data save successfully.')
            else:
                messages.error(request, 'Sorry, pleace try again the sent data is corrupt.')
            
        except Exception as e:
            messages.error(request, f'Sorry the following error has occured {e}')
        
        return render(request, self.templates_name, self.context)

class InvoiceVisualizationView(LoginRequiredSuperuserMixin, View):
    """this view helps to visualize the invoice"""
    
    template_name = 'invoice.html'
    
    def get(self, request, *args, **kwargs):
        
        pk = kwargs.get('pk')
        
        context = get_invoice(pk)
        
        return render(request, self.template_name, context)
    
@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    
    """ générer un fichier pdf à partir d'un fichier html """
    
    pk = kwargs.get('pk')
    
    context = get_invoice(pk)
    context['date'] = datetime.datetime.today()
    
    #fichier html (on crait le fichier html sans les liens dynamique)
    template = get_template('invoice_pdf.html')
    
    #envoi des variable de context directement dans le template
    html = template.render(context)
    
    #option du format pdf
    #option du format pdf
    options = {
        'page_size': 'letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': ''
    }
    
    #génération du pdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files (x86)\thirdparty\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    
    response['Content-Disposition'] = "attachement"
    
    return response
    
    