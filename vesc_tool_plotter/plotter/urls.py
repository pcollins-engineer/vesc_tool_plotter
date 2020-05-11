from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.upload, name="upload"),
    path("graph", views.graph, name="graph"),
    path("profile", views.profile, name="profile"),
    path("build", views.add_build, name="add_build")
]
