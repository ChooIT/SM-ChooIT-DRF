from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductViewset.as_view({"get": "list"}), name="product-list"),
    path('<int:pk>/', ProductViewset.as_view({"get": "retrieve"}, name="product-retrieve")),
    path('favorite/', create_user_favorite_product),
]
