from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import ProductListCreateAPIView

router=DefaultRouter()

# router.register(r'products', ProductListCreateAPIView,basename='product')
urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view()),
    path('orders/',views.orderListAPIView.as_view()),
    path('order-items/',views.orderItemListAPIView.as_view()),
    path('product-info/',views.product_info),  
    path('auth/register/',views.RegisterView.as_view(),name='register'),
    path('auth/login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'), 
]
urlpatterns += router.urls
