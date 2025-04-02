from django.conf import urls
from django.contrib import admin
from django.urls import path, include
from chibi_django.views import page_not_found
from chibi_django.snippet.url import show_urls

urls.handler404 = page_not_found


urlpatterns = [
    path( 'admin/', admin.site.urls ),
]

show_urls( urlpatterns )
