"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from catalog import views as catalog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalog_views.home, name='home'),
    path('promo/', catalog_views.promo_page, name='promo_page'),
    path('produit/<slug:slug>/', catalog_views.product_detail, name='product_detail'),
    path('produit/<slug:slug>/commander/', catalog_views.order_create, name='order_create'),
    path('commande/succes/<int:order_id>/', catalog_views.order_success, name='order_success'),
    path('categorie/<slug:category_slug>/', catalog_views.category_list, name='category_list'),
    path('panier/', catalog_views.cart_view, name='cart_view'),
    path('panier/ajouter/<int:product_id>/', catalog_views.cart_add, name='cart_add'),
    path('panier/supprimer/<int:product_id>/', catalog_views.cart_remove, name='cart_remove'),
    path('panier/vider/', catalog_views.cart_clear, name='cart_clear'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    # Serve media files in this Windows setup (local prod with Waitress).
    # For real production behind a web server, serve media via the web server instead.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', catalog_views.serve_media, name='media'),
    ]
