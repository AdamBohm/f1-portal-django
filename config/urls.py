from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('f1_app.urls')), # Tohle říká: "Všechno ostatní hledej v aplikaci f1_app"
]