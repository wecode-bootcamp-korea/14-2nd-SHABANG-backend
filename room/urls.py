from django.urls import path

from .views      import RoomMapView
urlpatterns = [
    path('/map', RoomMapView.as_view())
]