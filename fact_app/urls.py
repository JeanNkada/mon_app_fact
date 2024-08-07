
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add_customer', views.AddCustomerView.as_view(), name='add-customer'),
    path('add_invoice', views.AddInvoiceView.as_view(), name='add-invoice'),
    path('view-invoice/<int:pk>', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path('invoice_pdf/<int:pk>', views.get_invoice_pdf, name='invoice_pdf'),
    path('statistic', views.StatisticView.as_view(), name='statistic'),
    
]

