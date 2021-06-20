from django.urls import path
from .views import product

urlpatterns = [
    path('', product.ProductViewset.as_view({"get": "list"}), name="product-list"),
    path('<int:pk>/', product.ProductViewset.as_view({"get": "retrieve"}, name="product-retrieve")),
    path('favorite/', product.create_user_favorite_product),
]
