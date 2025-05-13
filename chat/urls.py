from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
urlpatterns = [
       path("chat/", views.index, name="index"),
       path("chat/<int:room_id>/", views.room, name="room"),
        path("auth/login/",
    LoginView.as_view(
        template_name="chat/LoginPage.html",
        redirect_authenticated_user=True,
        next_page='/chat'
    ),
    name="login-user",
),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path("auth/signup/", views.SignUpView.as_view(), name="signup"),
]