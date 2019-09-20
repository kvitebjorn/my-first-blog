"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/password_reset/', views.password_reset, name='password_reset', ),
    path('accounts/password_reset_done/', views.password_reset_done, name='password_reset_done', ),
    url('^accounts/password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.password_reset_confirm, name='password_reset_confirm', ),
    path('accounts/password_reset_complete/', views.password_reset_complete, name='password_reset_complete', ),

    path('accounts/', include('django_registration.backends.activation.urls')),
    # =============================================================================
    # From the documentation, need to implement a template for the following:
    #     django_registration_register is the account-registration view.
    #     django_registration_complete is the post-registration success message.
    #     django_registration_activate is the account-activation view.
    #     django_registration_activation_complete is the post-activation success message.
    #     django_registration_disallowed is a message indicating registration is not currently permitted.
    # =============================================================================

    
    path('', include('blog.urls')),
    path('markdownx/', include('markdownx.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT        
)