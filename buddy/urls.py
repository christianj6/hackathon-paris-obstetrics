"""hackathon_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.buddy, name='buddy-home'),
    path('', views.BoardListView.as_view(), name="BoardList"),
    path('boards/<int:pk>/', views.TopicListView.as_view(), name="TopicList"),
    path('boards/<int:pk>/new/', views.TopicCreateView.as_view(), name="NewTopic"),
    path('boards/<int:pk>/topics/<int:topic_pk>/',
         views.TopicPostsView.as_view(), name="TopicPosts"),
    path('boards/<int:pk>/topics/<int:topic_pk>/edit/<int:post_pk>/',
         views.PostUpdateView.as_view(), name="PostUpdate"),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/',
         views.PostReplyView.as_view(), name="PostReply"),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)