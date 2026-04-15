from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/',views.ProductDetailAPIView.as_view()),
    path('orders/',views.order_list),
    path('orderItem/',views.orderItem_list),
    path('product-info/',views.product_info),
]