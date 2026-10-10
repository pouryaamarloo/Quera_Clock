from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from apps.users.views import RegisterView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("login/",LoginView.as_view(template_name="../apps/users/registration/login.html"), name="login"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("register/",RegisterView.as_view(), name="register"),
    path("profile/",ProfileUpdateView.as_view(), name="profile"),


]