from django.urls import path

from apartment.views import ApartmentGraphView, ComplexDetailView, ApartmentMapView, ApartmentGraphView, SearchView


urlpatterns = [
    path('/graph/<int:id>', ApartmentGraphView.as_view()),
    path('/complex/<int:complex_id>', ComplexDetailView.as_view()),
    path('/map', ApartmentMapView.as_view()),
    path('/search', SearchView.as_view()),
]

