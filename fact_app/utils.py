
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from .models import *


def pagination(request, invoices):
    
    # page par defaut
    default_page =1
    
    page = request.GET.get('page', default_page)
    
    # nombre d'élément par page
    items_per_page = 5
    
    paginator = Paginator(invoices, items_per_page)
    
    #verification sur les pages
    try:
        
        items_page = paginator.page(page)
        
    except PageNotAnInteger:
        
        items_page = paginator.page(default_page)
        
    
    except EmptyPage:
        
        items_page = paginator.page(paginator.num_pages)
        
    return items_page

def get_invoice(pk):
    """get invoice fonction"""
        
    obj = Invoice.objects.get(pk=pk)
        
    articles = obj.article_set.all()
        
    context = {
        'obj': obj,
        'articles': articles
    }
    
    return context