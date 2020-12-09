from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('facility', include('facility.urls')),
    path('apartment', include('apartment.urls'))
]
