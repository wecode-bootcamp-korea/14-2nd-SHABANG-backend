import json, re

from haversine import haversine
from datetime  import datetime

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, Max, Min, Avg, Count

from .models          import Apartment, ApartmentComplex, District, Neighborhood, TradeType
from facility.models  import School

class ApartmentGraphView(View):
    def get(self, request, id):
        try:
            size_id    = request.GET.get('size_id', None)
            apartments = ApartmentComplex.objects.get(id=id).apartment_set.\
            values(
                'trade_year',
                'trade_month',
                'size_id',
                'trade_type_id'
                ).\
                annotate(
                    Avg('price'),
                    Count('price')
                    )
            trade_filter     = {'trade_type_id':3, 'size_id':size_id}
            rent_filter      = {'trade_type_id':2, 'size_id':size_id}
            trade_apartments = apartments.filter(**trade_filter)
            rent_apartments  = apartments.filter(**rent_filter)
            trade_years = trade_apartments.values('trade_year').distinct()
            rent_years = rent_apartments.values('trade_year').distinct()
            if not (rent_apartments or trade_apartments).exists():
                return JsonResponse({"message":"INVALID_SIZE_ID"}, status=400)

            trade_apartments_data = [{
                year['trade_year'] : [{
                    "date"   : str(row['trade_year'])+'. ' + str(row['trade_month']),
                    "values" : [int(row['price__avg']), row['price__count']]
                            } for row in trade_apartments if row['trade_year'] == year['trade_year']]
                            } for year in trade_years]

            rent_apartments_data = [{
                year['trade_year'] : [{
                    "date"   : str(row['trade_year'])+'. ' + str(row['trade_month']),
                    "values" : [int(row['price__avg']), row['price__count']]
                            } for row in rent_apartments if row['trade_year'] == year['trade_year']]
                            } for year in rent_years]

            return JsonResponse(
                {
                    "trade_apartments_data":trade_apartments_data,
                    "rent_apartments_data" :rent_apartments_data
                    }
                    , status=200)
        except ApartmentComplex.DoesNotExist:
            return JsonResponse({"message":"INVALID_APARTMENT_COMPLEX"}, status=400)
        except ValueError:
            return JsonResponse({"message":"INVALID_VALUE"}, status=400)
        except TypeError:
            return JsonResponse({"message":"INVALID_TYPE"}, status=400)

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
                        'square_decametre' : size.area,
                        'py'                : int(size.area/3.3),
                        'selling'           : apartments.filter(size_id=size.id, trade_type_id=3).aggregate(Avg('price'))['price__avg'],
                        'renting'           : apartments.filter(size_id=size.id, trade_type_id=2).aggregate(Avg('price'))['price__avg'],
                    }
                    for size in set(apartment.size for apartment in apartments.order_by('size_id'))
                ],

                'trade_data'      : [
                    {
                        'trade_date'       : f'{apartment.trade_year}.{apartment.trade_month}',
                        'floor'            : apartment.floor,
                        'pricePerP'        : int(int(apartment.price)/(apartment.size.area/3.3)),
                        'trade_type'       : apartment.trade_type.name,
                        'square_decametre' : apartment.size.area,
                        'py'               : int(apartment.size.area/3.3),
                    }
                        for apartment in apartments.order_by('-trade_year', '-trade_month')[:10]
                 ],
            }

            return JsonResponse({'complex': context}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class ApartmentMapView(View):
    def get(self, request):
        try:
            zoom_level    = request.GET.get('zoom_level', 4)
            latitude      = request.GET.get('latitude', 33.450701)
            longitude     = request.GET.get('longitude', 126.570667)
            trade_type    = request.GET.get('trade_type', 2)
            size1         = request.GET.get('size1', 1)
            size2         = request.GET.get('size2', 21)
            year          = request.GET.get('year')
            household_num = request.GET.get('household_num')

            q_complex   = Q()
            q_apartment = Q()

            q_apartment.add(Q(size_id__gt=int(size1)), Q.AND)
            q_apartment.add(Q(size_id__lt=int(size2)), Q.AND)

            if household_num:
                q_complex.add(Q(household_number__gt=household_num), Q.AND)

            if year:
                q_complex.add(Q(completion_year__lt=datetime.today().year-int(year)), Q.AND)

            if trade_type:
                q_apartment.add(Q(trade_type_id=int(trade_type)), Q.AND)

            complexes = [c for c in ApartmentComplex.objects.all().filter(q_complex) if [haversine((float(latitude), float(longitude)), (c.latitude, c.longitude), unit='km') < 10]]
            apartments = [apt for apt in Apartment.objects.all().filter(q_apartment) if [haversine((float(latitude), float(longitude)), (ApartmentComplex.objects.get(id=apt.apartment_complex_id).latitude, ApartmentComplex.objects.get(id=apt.apartment_complex_id).longitude), unit='km') < 6]]

            complex_neighborhoods = set(apartment.neighborhood for apartment in apartments)
            complex_districts     = set(apartment.district for apartment in apartments)

            if int(zoom_level) < 5:
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

            if int(zoom_level) == 5 or int(zoom_level) == 6:
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

                complex_neighborhoods = [n for n in Neighborhood.objects().all() if haversine((float(latitude),float(longitude)), (n.latitude, n.longitude), unit='km') < 10]
                context = [
                    {
                        'neighborhood_id': neighborhood.id,
                        'neighborhood_name': neighborhood.name,
                        'latitude': neighborhood.latitude,
                        'longitude': neighborhood.longitude,
                        'average_price': '-', 
                    }
                        for neighborhood in complex_neighborhoods
                ]

                return JsonResponse({'result':context}, status=200)

            if int(zoom_level) == 7:
                if complexes:
                    context = [
                        {
                            'district_id'  : district.id ,
                            'district_name': district.name,
                            'latitude'     : district.latitude,
                            'longitude'    : district.longitude,
                            'average_price': Apartment.objects.filter(district_id=district.id).aggregate(Avg('price'))['price__avg'] 
                        }
                            for district in complex_districts
                    ]

                    return JsonResponse({'result': context}, status=200)

                complex_districts = [d for d in District.objects().all() if haversine((float(latitude),float(longitude)),(d.latitude, d.longitude),unit='km') < 10]

                context = [
                    {
                        'district_id'  : district.id ,
                        'district_name': district.name,
                        'latitude'     : district.latitude,
                        'longitude'    : district.longitude,
                        'average_price': '-' 
                    }
                        for district in complex_districts
                ]

                return JsonResponse({'result': context}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
