from django.urls import path

from facility.views import NearFacilityView

urlpatterns = [
    path("/<int:id>", NearFacilityView.as_view())
]