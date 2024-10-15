from django.urls import path

from loginapp.views import LoginAndSaveCookiesView

urlpatterns = [
    path("setcookie/", LoginAndSaveCookiesView.as_view()),
]
