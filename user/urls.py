from django.urls import path

from .views      import KakaoLogInView, GoogleLogInView

urlpatterns = [
    path('/kakaologin', KakaoLogInView.as_view()),
    path('/googlelogin', GoogleLogInView.as_view()),
]
