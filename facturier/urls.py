
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    
]
urlpatterns += i18n_patterns(
    path('', include('fact_app.urls')),
)

if settings.DEBUG:
    
    urlpatterns+=static(settings.MEDIA_URL, document_ROOT=settings.MEDIA_ROOT)
