import os
import django
from django.conf import settings

# Ustawianie DJANGO_SETTINGS_MODULE na wartość pliku settings.py w Twojej aplikacji Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekt.settings')
django.setup()

# Pozostała część Twojego kodu
from django.contrib import admin
from django.urls import path
from views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]
