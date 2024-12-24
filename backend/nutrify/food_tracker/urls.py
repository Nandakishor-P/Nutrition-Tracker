from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


urlpatterns = [
    path('', views.nutrition, name='home'),
        # Home page view
    path('login', views.user_login, name='login'),
    path('about.html', views.about_author, name='about_author'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('log_food/', views.log_food, name='log_food'),
    path('water-intake/', views.track_water_intake, name='water-intake'),
    path('set-goals/', views.set_goals, name='set_goals'),
    path('save-goals/', views.save_goals, name='save_goals'),
    path('change-password/', login_required(PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url=reverse_lazy('login') 
    )), name='change_password'),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
