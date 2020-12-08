from haversine import haversine

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from facility.models import School, Subway, ConvenientStore, Cafe
from apartment.models import ApartmentComplex

class NearFacilityView(View): 
    def get(self, request, id):
        try:
            apartment_complex = ApartmentComplex.objects.get(id=id)
            latitude = float(apartment_complex.latitude)
            longitude = float(apartment_complex.longitude)
            position      = (latitude,longitude)
            LATITUDE_1KM  = 0.00904
            LONGITUDE_1KM = 0.00898
            if not (-90 < latitude < 90 and -180 < longitude < 180):
                return JsonResponse({"message":"INVALID_COORDINATE"}, status=400)
            limit = (
                Q(latitude__gt=latitude-LATITUDE_1KM, latitude__lt=latitude+LATITUDE_1KM) &
                Q(longitude__gt=longitude-LONGITUDE_1KM, longitude__lt=longitude+LONGITUDE_1KM)
            )

            schools = School.objects.filter(limit)
            near_schools = [school for school in schools if haversine(position, (school.latitude, school.longitude)) < 1 ]
            school_data = [{
                "id"        : school.id,
                "name"      : school.name,
                "latitude"  : school.latitude,
                "longitude" : school.longitude,
                "distance"  : int(haversine(position, (school.latitude, school.longitude), unit='m'))
            }for school in near_schools]

            subways = Subway.objects.select_related("subway_line").filter(limit)
            near_subways = [subway for subway in subways if haversine(position, (subway.latitude, subway.longitude)) < 1]
            subway_data = [{
                "id"        : subway.id,
                "name"      : subway.name,
                "latitude"  : subway.latitude,
                "longitude" : subway.longitude,
                "distance"  : int(haversine(position, (subway.latitude, subway.longitude), unit='m'))
            }for subway in near_subways]

            convenient_stores = ConvenientStore.objects.filter(limit)
            near_convenient_stores = [store for store in convenient_stores if haversine(position, (store.latitude, store.longitude)) < 1]
            convenient_store_data = [{
                "id"        : store.id,
                "name"      : store.name,
                "latitude"  : store.latitude,
                "longitude" : store.longitude,
                "distance"  : int(haversine(position, (store.latitude, store.longitude), unit='m'))
            }for store in near_convenient_stores]

            cafes = Cafe.objects.filter(limit)
            near_cafes = [cafe for cafe in cafes if haversine(position, (cafe.latitude, cafe.longitude)) < 1]
            cafe_data = [{
                "id"        : cafe.id,
                "name"      : cafe.name,
                "latitude"  : cafe.latitude,
                "longitude" : cafe.longitude,
                "distance"  : int(haversine(position, (cafe.latitude, cafe.longitude), unit='m'))
            }for cafe in near_cafes]

            return JsonResponse(
                {
                    "school"           : school_data,
                    "subway"           : subway_data,
                    "convenient_store" : convenient_store_data,
                    "cafe"             : cafe_data,
                    }
                    ,status=200)
        except ValueError:
            return JsonResponse({"message":"INVALID_VALUE"}, status=400)
        except TypeError:
            return JsonResponse({"message":"INVALID_TYPE"}, status=400)

