from django.urls import path

from loginapp.views import LoginAndSaveCookiesView

urlpatterns = [
    path("runapp/", LoginAndSaveCookiesView.as_view()),
]
