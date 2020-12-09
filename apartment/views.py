from django.views import View
from django.http import JsonResponse
from django.db.models import Avg, Count

from apartment.models import ApartmentComplex

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