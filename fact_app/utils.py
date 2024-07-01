
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


def pagination(request, invoices):
    
    # page par defaut
    default_page =1
    
    page = request.GET.get('page', default_page)
    
    # nombre d'élément par page
    items_per_page = 5
    
    paginator = Paginator(invoices, items_per_page)
    
    #verification sur les page
    try:
        
        items_page = paginator.page(page)
        
    except PageNotAnInteger:
        
        items_page = paginator.page(default_page)
        
    
    except EmptyPage:
        
        items_page = paginator.page(paginator.num_pages)
        
    return items_page