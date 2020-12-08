from haversine        import haversine
import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from user.models      import User, Favor
from .models          import (
    Room, 
    Image, 
    Agency, 
    Status, 
    FloorType, 
    RoomType, 
    StructureType, 
    Parking, 
    Direction
)
from apartment.models import (
    Apartment, 
    ApartmentComplex, 
    District, 
    Neighborhood, 
    TradeType, 
    Size
    ) 

class RoomMapView(View):
    def get(self, request):
        try:
            tradetype     = request.GET.get('tradetype', None) 
            deposit_gteq  = request.GET.get('deposit_gteq', None) 
            deposit_lteq  = request.GET.get('deposit_lteq', None) 
            structuretype = request.GET.get('structuretype', None) 
            roomtype      = request.GET.get('roomtype', None) 
            parking       = request.GET.get('parking', None) 
            center_lat    = request.GET.get('center_lat', None) 
            center_lng    = request.GET.get('center_lng', None) 
            zoom_level    = request.GET.get('zoom_level', None) 

            zoom_level = int(zoom_level)
            center_lat = float(center_lat)
            center_lng = float(center_lng)

            zoom_level_list = [0,0.5,1.0,2.0,2.5,3.0,3.5,4.0,4.5]

            center_point = (center_lat, center_lng)
            zoom_level_now = zoom_level_list[zoom_level]

            rooms = Room.objects.select_related(
                    'agency',
                    'direction',
                    'status',
                    'floor_type',
                    'room_type',
                    'structure_type',
                    'parking',
                    'trade_type'
            ).prefetch_related(
                'image_set')

            q = Q()
                
            if tradetype:
                q.add(Q(trade_type__name=tradetype), Q.AND)

            if deposit_lteq:
                q.add(Q(deposit__gte=deposit_lteq), Q.AND)

            if deposit_gteq:
                q.add(Q(deposit__lte=deposit_gteq), Q.AND)

            if structuretype:
                q.add(Q(structure_type__name=structuretype), Q.AND)

            if roomtype:
                q.add(Q(room_type__name=roomtype), Q.AND)

            if parking:
                q.add(Q(parking__count=parking), Q.AND)

            oneroom_list = [
            {
                'room_id'         : room.id,
                'region'          : room.address,
                'lat'             : room.latitude,
                'lng'             : room.longitude,
                'thumbnail_img'   : room.image_set.all()[0].image_url,
                'detail_img'      : 
                [
                    {
                        'img_id'  : img.id,
                        'img_url' : img.image_url } for img in room.image_set.all()],
                'type'            : room.structure_type.name,
                'price'           : [{
                    'trade_type'  : room.trade_type.name,
                    'deposit'     : room.deposit,
                    'rent'        : room.rent
                }],
                'space'           : room.area,
                'floor'           : room.floor,
                'description'     : room.description,
                'parking'         : room.parking.count,
                'distance'        : haversine(center_point, (room.latitude, room.longitude), unit='km')

            } 
            for room in rooms.filter(q) if haversine(center_point, (room.latitude, room.longitude), unit='km') < zoom_level_now
        ]
        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=404)

        return JsonResponse(
            {
                'total_count' : len(oneroom_list),
                'oneroom' : oneroom_list,
            }, status=200
        )