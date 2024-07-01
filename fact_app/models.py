from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    """
        name = customer models definition 
    """
    SEX_TYPE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=128)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPE)
    age = models.CharField(max_length=16)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    def __str__(self):
        return self.name
    


class Invoice(models.Model):
    
    """
    name =  Invoice models definition
    description=
    author=
    """
    INVOICE_TYPE = (
        ('R', 'RECEIPT'),
        ('I', 'INVOICE'),
        ('P', 'PROFORMA INVOICE')
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)  
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    last_update_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comment = models.TextField(null=True, blank=True, max_length=1000)
    
    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    def __str__(self):
        return f"{self.customer.name}_{self.invoice_date_time}"
    
    @property
    def get_tolal(self):
        articles =self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total
    
    
class Article(models.Model):

    """
    name =  product models definition
    """
    name = models.CharField(max_length=120)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    def __str__(self):
        return self.name
    
    @property
    def get_tolal(self):
        total = self.quantity*self.unit_price
        return total