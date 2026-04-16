from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('ajax/delete-product-image/<int:image_id>/', views.delete_product_image_ajax, name='delete_product_image_ajax'),
]
