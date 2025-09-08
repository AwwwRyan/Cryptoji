from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.encrypt_message, name='encrypt'),
    path('decrypt/', views.decrypt_message, name='decrypt'),
]
