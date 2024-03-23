from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("random/", views.random, name="random"),
    path("edit/", views.edit, name="edit")
]