from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.upload, name="upload"),
    path("graph/", views.graph, name="graph"),
    path("graph/<int:ride_id>/", views.graph, name="graph"),
    path("profile/<username>/", views.profile, name="profile"),
    path("build/", views.add_build, name="add_build"),
    path(r'^profile/<username>/<build>/<form>/edit$', views.edit_build, name="edit_build"),
]
