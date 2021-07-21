from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='example-home'),
    path('about/', views.about, name='example-about')
    # path('about/', views.about, name='example-about')
]

urlpatterns += staticfiles_urlpatterns()