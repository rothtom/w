
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("get_posts/<str:category>/<int:page_number>", views.get_posts, name="get_posts"),
    path("posts/<str:category>/<int:page_number>", views.display_posts, name="display_posts"),
    path("profile/<str:username>", views.profile, name="profile"),
]
