import json

from .models          import Room, Image, Agency, Status, FloorType, RoomType, StructureType, Parking, Direction
from apartment.models import District, Neighborhood, TradeType

from django.test       import TestCase
from django.test       import Client
from unittest.mock     import patch, MagicMock

class RoomTest(TestCase):
    maxDiff = None
    def setUp(self):
        client = Client()
        
        TradeType.objects.create(
            id   = 1,
            name = '월세'
        )

        Agency.objects.create(
            id   = 1,
            name = '위코드부동산',
            phone_number = '010-1234-5678',
            image_url = 'https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/logo/title_img1.png'
        )

        Status.objects.create(
            id   = 1,
            status = '거래중'
        )

        FloorType.objects.create(
            id   = 1,
            name = '지상층'
        )

        RoomType.objects.create(
            id   = 1,
            name = '단독주택'
        )

        StructureType.objects.create(
            id   = 1,
            name = '오픈형 원룸'
        )

        Parking.objects.create(
            id   = 1,
            count = '1대 가능'
        )

        Direction.objects.create(
            id   = 1,
            name = '동향'
        )

        Room.objects.create(
            id               = 1,
            longitude        = str('127.029462812382000'),
            latitude         = str('37.510034821369400'),
            register_number  = 24992883,
            area             = str('29.59000'),
            completion_year  = '2004-04-14',
            deposit          = str('1000.0000'),
            rent             = str('80.0000'),
            maintenance_cost = str('5.0000'),
            top_floor  = 5,
            floor  = 2,
            description  = '전세대출가능 최저가 약속, 채광 좋은 매물',
            address  = '강남구 논현동 155-3',
            available_date  = '37.518740000000001',
            trade_type_id  = 1,
            agency_id  = 1,
            status_id  = 1,
            floor_type_id  = 1,
            room_type_id  = 1,
            structure_type_id  = 1,
            parking_id  = 1,
            direction_id  = 1,
            has_elevator  = True,
        )

        Image.objects.create(
            id   = 1,
            image_url = 'https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/logo/title_img1.png',
            room_id = 1
        )

    def tearDown(self):
        Room.objects.all().delete()
        Image.objects.all().delete()
        Agency.objects.all().delete()
        Status.objects.all().delete()
        FloorType.objects.all().delete()
        RoomType.objects.all().delete()
        StructureType.objects.all().delete()
        Parking.objects.all().delete()
        Direction.objects.all().delete()
        District.objects.all().delete()
        Neighborhood.objects.all().delete()
        TradeType.objects.all().delete()


    def test_room_get_success(self):
        client = Client()

        response = client.get('/room/map?center_lat=37.505169&center_lng=127.050346&zoom_level=7')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'total_count' : 1,
            'oneroom':[
                {
                    'room_id':1,
                    'region':'강남구 논현동 155-3',
                    'lat':str('37.510034821369400'),
                    'lng':str('127.029462812382000'),
                    'thumbnail_img':'https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/logo/title_img1.png',
                    'detail_img'      : 
                [
                    
                        {'img_id'  : 1,
                        'img_url' : 'https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/logo/title_img1.png',
                        }],
                'type'            : '오픈형 원룸',
                'price'           : [{
                    'trade_type'  : '월세',
                    'deposit'     : str('1000.0000'),
                    'rent'        : str('80.0000')
                }],
                'space'           : str('29.59000'),
                'floor'           : 2,
                'description'     : '전세대출가능 최저가 약속, 채광 좋은 매물',
                'parking'         : '1대 가능',
                'distance'        : 1.9198807205251933

        }]})

    def test_room_get_fail(self):
        client = Client()
        response = client.get('/room/map?center_lat=37.505169')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                'message':'TYPE_ERROR'
            }
        )

    def test_room_get_not_found(self):
        client = Client()

        response = client.get('/room/map123')

        self.assertEqual(response.status_code, 404)