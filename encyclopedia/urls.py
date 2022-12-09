from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("bar/", views.bar, name="bar"),
    path("page/", views.page, name="page"),     
]
