from django.urls import path
from .API import signup, login


urlpatterns = [
    path('email/', signup.is_registered_email),
    path('signup/', signup.create_user),
    path('tag/', signup.create_new_favorite_tag),
    path('login/', login.LoginView.as_view()),
]
