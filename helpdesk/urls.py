from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy, include
from django.conf import settings
from django.conf.urls.static import static

from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'accounts/login/', CustomLoginPage.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    # path('accounts/profile/', , name='profile'),

    # path('finder/', advanced_finder, name='advanced-finder'),

    path('base/', include('base.urls', namespace='base')),

    path('exploitation/', include('exploitation.urls', namespace='exploitation')),
    path('build/', include('build.urls', namespace='build')),
    path('maintenance/', include('maintenance.urls', namespace='maintenance')),

    path('', dashboard, name='dashboard'),
]
