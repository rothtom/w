from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("delete_listing", views.delete_listing, name="delete_listing"),
    path("bid", views.bid, name="bid")
]
