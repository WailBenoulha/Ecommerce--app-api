from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ecomm import views


router =DefaultRouter()
router.register('product',views.ProductViewSet)
router.register('order',views.OrderViewSet)
router.register('tag',views.TagViewSet)

urlpatterns = [
    path('',include(router.urls)),
]