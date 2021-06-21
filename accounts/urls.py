from django.urls import path
from .views import signup, profile
from rest_framework_jwt.views import ObtainJSONWebToken


urlpatterns = [
    path('email/', signup.is_registered_email),
    path('signup/', signup.create_user),
    path('signup/tag/', signup.create_new_favorite_tag),
    path('signup/product/', signup.create_using_prod_history),
    path('login/', profile.LoginView.as_view()),
    path('detail/', profile.get_profile_detail),
]
