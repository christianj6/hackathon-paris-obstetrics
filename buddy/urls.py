from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.recommended_buddies_view, name="buddy-home"),
    path("buddy-invite/", views.send_buddy_request, name="buddy-invite"),
    path("buddy-cancel/", views.delete_buddy_request, name="buddy-cancel"),
    path("buddy-ignore/", views.ignore_buddy_request, name="buddy-ignore"),
    path("buddy-accept/", views.accept_buddy_request, name="buddy-accept"),
    path("buddy-board/", views.buddy_board_view, name="buddy-board"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
