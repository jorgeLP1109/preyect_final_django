"""
URL configuration for ventas_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .views import register, product_list, product_detail, create_product, edit_product, CustomLoginView, CustomLogoutView, home, otra_vista, custom_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView




urlpatterns = [
    #path('home/', home, name='home'),
    #path('products/', product_list, name='product_list'),
    path('product_list/', product_list, name='product_list'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    
    #path('', product_list, name='product_list'),
    path('', home, name='home'),

    path('productos/crear/', create_product, name='create_product'),
    path('productos/editar/<int:id_producto>/', edit_product, name='edit_product'),
    #path('editar_producto/<int:id_producto>/', edit_product, name='edit_product'),
    path('login/', LoginView.as_view(), name='login'),
    path('custom-login/', CustomLoginView.as_view(), name='custom_login'),
    #path('custom-login/', custom_login, name='custom_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    #path('products/', include('ventas_web.urls')),
    path('otra_vista/', otra_vista, name='otra_vista'),

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
