from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from buddy import views as buddy_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("register/", user_views.register, name="register"),
    path("practice/", user_views.practice, name="practice"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "practice/update-proficiency/",
        user_views.update_proficiency,
        name="update-proficiency",
    ),
    path(
        "practice/save-resource/",
        user_views.save_to_board,
        name="save-resource",
    ),
    path("practice/assessment/", user_views.assessment, name="assessment"),
    path("buddy/", include("buddy.urls")),
    path("", include("home.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
