from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='example-home'),
    path('about/', views.about, name='example-about')
    # path('about/', views.about, name='example-about')
]