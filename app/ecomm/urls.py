from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from ecomm import views


urlpatterns = [
    path('latest-products/',views.LatestProductList.as_view()),
    path('category',views.CategoryView.as_view())
]