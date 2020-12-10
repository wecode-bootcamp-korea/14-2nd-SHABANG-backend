from django.urls import path

from apartment.views import ApartmentGraphView, SearchView

urlpatterns = [
    path('/graph/<int:id>', ApartmentGraphView.as_view()),
    path('/search', SearchView.as_view())
]