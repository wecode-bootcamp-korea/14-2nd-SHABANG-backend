import json, re

from haversine import haversine
from datetime  import datetime

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, Max, Min, Avg

from .models          import Apartment, ApartmentComplex, District, Neighborhood, TradeType

class ComplexDetailView(View):
    def get(self, request, complex_id):
        try:
            apartment_complex = ApartmentComplex.objects.prefetch_related('apartment_set').get(id=complex_id)
            apartments        = apartment_complex.apartment_set.all()

            context = {
                'complex_id'      : complex_id,
                'complex_name'    : apartment_complex.name,
                'completion_year' : apartment_complex.completion_year,
                'image_url'       : apartment_complex.image_url,
                'household_number': apartment_complex.household_number,
                'address'         : apartment_complex.address,
                'size'            : [
                    {
                        'm^2'     : size.area,
                        'p'       : int(size.area/3.3),
                        'selling' : apartments.filter(size_id=size.id, trade_type_id=3).aggregate(Avg('price'))['price__avg'],
                        'renting' : apartments.filter(size_id=size.id, trade_type_id=2).aggregate(Avg('price'))['price__avg'],
                    }
                    for size in set(apartment.size for apartment in apartments.order_by('size_id'))
                ],

                'trade_data'      : [
                    {
                        'trade_date' : f'{apartment.trade_year}.{apartment.trade_month}',
                        'floor'      : apartment.floor,
                        'pricePerP'  : int(int(apartment.price)/(apartment.size.area/3.3)),
                        'trade_type' : apartment.trade_type.name,
                        'm^2'        : apartment.size.area,
                        'p'          : int(apartment.size.area/3.3),
                    }
                        for apartment in apartments.order_by('-trade_year', '-trade_month')[:10]
                 ],
            }

            return JsonResponse({'complex': context}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class ApartmentMapView(View):
    def post(self, request):
        try:
            zoom_level    = int(request.GET.get('zoom_level'))
            longitude     = request.GET.get('longitude')
            latitude      = request.GET.get('latitude')
            x1            = request.GET.get('x1')
            x2            = request.GET.get('x2')
            y1            = request.GET.get('y1')
            y2            = request.GET.get('y2')
            trade_type    = request.GET.get('trade_type')
            size1         = int(request.GET.get('size1'))
            size2         = int(request.GET.get('size2'))
            year          = request.GET.get('year')
            household_num = request.GET.get('household_num')

            q_complex   = Q()
            q_apartment = Q()

            if trade_type:
                q_apartment.add(Q(trade_type_id=int(trade_type)), Q.AND)

            if household_num:
                q_complex.add(Q(household_number__gt=household_num), Q.AND)

            if year:
                q_complex.add(Q(completion_year__lt=datetime.today().year-int(year)), Q.AND)

            if size1 and size2:
                q_apartment.add(Q(size_id__gt=size1), Q.AND)
                q_apartment.add(Q(size_id__lt=size2), Q.AND)

            if trade_type:
                q_apartment.add(Q(trade_type_id=int(trade_type)), Q.AND)

            complexes     = ApartmentComplex.objects.prefetch_related('apartment_set').filter(latitude__range=(x1,x2), longitude__range=(y1,y2)).filter(q_complex)

            apartments            = [c.apartment_set.all()[0] for c in complexes]
            complex_neighborhoods = set(apartment.neighborhood for apartment in apartments)
            complex_districts     = set(neighborhood.district for neighborhood in complex_neighborhoods)

            if zoom_level < 5:
                if not complexes:
                    return JsonResponse({'message':'NO_DATA'}, status=200)

                context = {
                    '10'  : [
                        {
                            'complex_id'        : c.id,
                            'complex_name'      : c.name,
                            'complex_latitude'  : c.latitude,
                            'complex_longitude' : c.longitude,
                            'max_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__lt=1000000000).aggregate(Max('price'))['price__max']),
                            'min_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__lt=1000000000).aggregate(Min('price'))['price__min'])
                        }
                            for c in complexes if Apartment.objects.filter(apartment_complex_id=c.id, price__lt=1000000000)
                    ],
                    '20'  : [
                        {
                            'complex_id'        : c.id,
                            'complex_name'      : c.name,
                            'complex_latitude'  : c.latitude,
                            'complex_longitude' : c.longitude,
                            'max_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__range=(1000000000,2000000000)).aggregate(Max('price'))['price__max']),
                            'min_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__range=(1000000000,2000000000)).aggregate(Min('price'))['price__min'])
                        }
                            for c in complexes if Apartment.objects.filter(apartment_complex_id=c.id, price__range=(1000000000,2000000000))
                    ],
                    '30'  : [
                        {
                            'complex_id'        : c.id,
                            'complex_name'      : c.name,
                            'complex_latitude'  : c.latitude,
                            'complex_longitude' : c.longitude,
                            'max_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__range=(2000000000,3000000000)).aggregate(Max('price'))['price__max']),
                            'min_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__range=(2000000000,3000000000)).aggregate(Min('price'))['price__min'])
                        }
                            for c in complexes if Apartment.objects.filter(apartment_complex_id=c.id, price__range=(2000000000, 3000000000))
                    ],
                    'rest': [
                        {
                            'complex_id'        : c.id,
                            'complex_name'      : c.name,
                            'complex_latitude'  : c.latitude,
                            'complex_longitude' : c.longitude,
                            'max_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__gt=(3000000000)).aggregate(Max('price'))['price__max']),
                            'min_price'         : int(Apartment.objects.filter(apartment_complex_id=c.id, price__gt=(3000000000)).aggregate(Min('price'))['price__min'])
                        }
                            for c in complexes if Apartment.objects.filter(apartment_complex_id=c.id, price__gt=3000000000)
                    ]
                }

                return JsonResponse({'result':context}, status=200)

            if zoom_level == 5 or zoom_level == 6:
                if complexes:
                    context = [
                        {
                            'neighborhood_id'  : neighborhood.id,
                            'neighborhood_name': neighborhood.name,
                            'latitude'         : neighborhood.latitude,
                            'longitude'        : neighborhood.longitude,
                            'average_price'    : Apartment.objects.filter(neighborhood_id=neighborhood.id).aggregate(Avg('price'))['price__avg']
                        }
                            for neighborhood in complex_neighborhoods
                    ]

                    return JsonResponse({'result':context}, status=200)

                complex_neighborhoods = Neighborhood.objects.filter(latitude__range=(x1,x2), longitude__range=(y1,y2))

                context = [
                    {
                        'neighborhood_id': neighborhood.id,
                        'neighborhood_name': neighborhood.name,
                        'latitude': neighborhood.latitude,
                        'longitude': neighborhood.longitude,
                        'average_price': None 
                    }
                        for neighborhood in complex_neighborhoods
                ]

                return JsonResponse({'result':context}, status=200)

            if zoom_level == 7:
                if complexes:
                    context = [
                        {
                            'district_id'  : district.id ,
                            'district_name': district.name,
                            'latitude'     : district.latitude,
                            'longitude'    : district.longitude,
                            'average_price': [Apartment.objects.filter(neighborhood_id=neighborhood.id).aggregate(Avg('price'))['price__avg'] for neighborhood in Neighborhood.objects.filter(district_id=district.id)]
                        }
                            for district in complex_districts
                    ]Apartment.objects.filter(neighborhood_id=neighborhood.id).aggrega

                        Neighborhood.objects.filter(district_id=district.id)
                    return JsonResponse({'result': context}, status=200)


                context = [
                    {
                        'district_id'  : district.id ,
                        'district_name': district.name,
                        'latitude'     : district.latitude,
                        'longitude'    : district.longitude,
                        'average_price': None 
                    }
                        for district in complex_districts
                ]

                return JsonResponse({ 'result': context}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
