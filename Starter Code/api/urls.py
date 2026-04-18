from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router=DefaultRouter()

router.register(r'products', ProductViewSet)
urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/',views.ProductDetailAPIView.as_view()),
    path('orders/',views.orderList.as_view()),
    path('order-items/',views.orderItemList.as_view()),
    path('product-info/',views.product_info),  
    path('auth/register/',views.RegisterView.as_view(),name='register'),
    path('auth/login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'), 
]
urlpatterns += router.urls
