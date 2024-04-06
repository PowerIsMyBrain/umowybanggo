# Plik views.py

# Wymagane importy Django
from django.http import HttpResponse

# Widok główny aplikacji
def home(request):
    return HttpResponse("To jest strona home")
