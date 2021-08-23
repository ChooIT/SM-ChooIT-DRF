from django.urls import path
from .views import product, review, data, recommendation

urlpatterns = [
    # main
    path('', recommendation.tag_filtering_product_list),
    path('populariest/', recommendation.get_item_list_of_the_day),
    path('search/', recommendation.get_item_list_filtered_by_category),

    # recommendation
    path('alike/user/', recommendation.get_recommendation_list_based_on_alike_user),
    path('alike/item/', recommendation.get_recommendation_list_based_on_alike_item),
    path('alike/mix/', recommendation.get_recommendation_list_based_on_mix),

    # product
    path('<int:pk>/', product.get_product_detail),
    path('favorite/', product.create_user_favorite_product),

    # review
    path('image/', review.post_review_image),
    path('review/', review.review_list),
    path('review/post/', review.post_new_review),
    path('review/<int:pk>/', review.ReviewDetail.as_view()),

    # category
    path('category/', data.CategoryList.as_view()),
    # tag
    path('tag/', data.TagList.as_view()),
]
