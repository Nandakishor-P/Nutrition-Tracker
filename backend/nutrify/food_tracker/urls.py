from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.nutrition, name='home'),
        # Home page view
    path('login/', views.nutrition, name='login'),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
