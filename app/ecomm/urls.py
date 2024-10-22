from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from ecomm import views


urlpatterns = [
    path('latest-products/',views.LatestProductList.as_view()),
    path('products/search',views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/',views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/',views.CategoryDetail.as_view()),
]