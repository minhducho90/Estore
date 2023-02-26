from django.urls import path
from . import views


app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('subcategory/<slug:slug>/', views.productlist, name="product-list"),
    path('product/<int:pk>/', views.productdetail, name='product-detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('product_api/', views.api_update_product),
    path('api/products/', views.products_service),
    path('api/products/<int:pk>/', views.products_service_detail),
]