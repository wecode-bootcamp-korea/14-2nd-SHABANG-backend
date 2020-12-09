from django.urls import path

from apartment.views import ApartmentGraphView

urlpatterns = [
    path('/graph/<int:id>', ApartmentGraphView.as_view())
]