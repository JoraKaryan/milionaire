from . import views
from django.urls import path

urlpatterns = [
    path('questions/', views.ChooseQuestion, name='questions'),
]
