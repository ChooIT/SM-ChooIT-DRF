from django.urls import path
from .views import product, review, data

urlpatterns = [
    path('', product.tag_filtering_product_list),
    path('<int:pk>/', product.get_product_detail),
    path('favorite/', product.create_user_favorite_product),
    path('image/', review.post_review_image),
    path('review/', review.review_list),
    path('review/post/', review.post_new_review),
    path('review/<int:pk>/', review.ReviewDetail.as_view()),
    path('category/', data.CategoryList.as_view()),
    path('tag/', data.TagList.as_view()),
]
