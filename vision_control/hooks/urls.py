from django.urls import path

from . import views

urlpatterns = [path("gitlab/", views.gitlab)]
