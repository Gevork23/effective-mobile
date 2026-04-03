from django.urls import path

from apps.accounts.views import DeleteAccountView, LoginView, LogoutView, ProfileView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", ProfileView.as_view()),
    path("delete/", DeleteAccountView.as_view()),
]
