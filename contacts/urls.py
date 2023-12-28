from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("new", views.new, name='new'),
    path("count", views.count, name='index'),
    path("<int:contact_id>/view", views.view, name='view'),
    path("<int:contact_id>/edit", views.edit, name='edit'),
    path("<int:contact_id>", views.delete, name='delete'),
]
