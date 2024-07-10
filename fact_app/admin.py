from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.

class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'age', 'sex', 'city', 'zip_code')

class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer', 'save_by', 'invoice_date_time', 'total', 'last_update_date', 'paid', 'invoice_type')
    
class AdminArticle(admin.ModelAdmin):
    list_display = ('name', 'invoice', 'quantity', 'unit_price', 'total')
    
admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article, AdminArticle)

admin.site.site_title= _('JBN INVOICE SYSTEM')
admin.site.site_header= _('JBN INVOICE SYSTEM')
admin.site.index_title= _('JBN INVOICE SYSTEM')
