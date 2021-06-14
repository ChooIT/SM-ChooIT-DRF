from django.urls import path
from .views import ProductViewset

urlpatterns = [
    path('', ProductViewset.as_view({"get": "list"}), name="product-list"),
    path('<int:pk>/', ProductViewset.as_view({"get": "retrieve"}, name="product-retrieve")),
]
