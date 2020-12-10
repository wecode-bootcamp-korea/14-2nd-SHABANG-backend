from django.urls import path

from .views      import ComplexDetailView, ApartmentMapView

urlpatterns = [
    path('/complex/<int:complex_id>', ComplexDetailView.as_view()),
    path('/map', ApartmentMapView.as_view()),
]
