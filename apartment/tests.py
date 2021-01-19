
from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock

from apartment.models import ApartmentComplex, Apartment, District, Neighborhood, TradeType, Size

class ApartmentGraphTest(TestCase):

    maxDiff = None

    def setUp(self):
        client = Client()

        ApartmentComplex.objects.create(
            id               = 99,
            name             = 'wecode아파트1',
            household_number = 1234,
            completion_year  = 2020,
            address          = '서울시 위코드동',
            latitude         = 37.518740000000001,
            longitude        = 127.020550000000001
        )

        Neighborhood.objects.create(
            id        = 1,
            name      = "강남구",
            latitude  = 37.523433300000005,
            longitude = 127.024074900000006
        )

        District.objects.create(
            id              = 1,
            name            = "압구정동",
            latitude        = 37.523433300000005,
            longitude       = 127.024074900000006,
        )

        TradeType.objects.create(
            id   = 3,
            name = '매매'
        )

        TradeType.objects.create(
            id   = 2,
            name = "전세"
        )

        Size.objects.create(
            id   = 40,
            area = '108'
        )

        Apartment.objects.create(
            price                = 6000,
            top_floor            = 22,
            floor                = 18,
            apartment_complex_id = 99,
            district_id          = 1,
            trade_type_id        = 3,
            trade_month          = 6,
            trade_year           = 2019,
            size_id              = 3
        )

        Apartment.objects.create(
            price                = 7000,
            top_floor            = 22,
            floor                = 12,
            apartment_complex_id = 99,
            district_id          = 1,
            trade_type_id        = 3,
            trade_month          = 11,
            trade_year           = 2020,
            size_id              = 3
        )

        Apartment.objects.create(
            price                = 8000,
            top_floor            = 22,
            floor                = 6,
            apartment_complex_id = 99,
            district_id          = 1,
            trade_type_id        = 3,
            trade_month          = 12,
            trade_year           = 2020,
            size_id              = 3
        )

        Apartment.objects.create(
            id                   = 25,
            price                = 3000,
            top_floor            = 22,
            floor                = 8,
            apartment_complex_id = 99,
            district_id          = 1,
            trade_type_id        = 2,
            trade_month          = 3,
            trade_year           = 2019,
            size_id              = 3
        )

        Apartment.objects.create(
            id                   = 22,
            price                = 4000,
            top_floor            = 22,
            floor                = 3,
            apartment_complex_id = 99,
            district_id          = 1,
            trade_type_id        = 2,
            trade_month          = 11,
            trade_year           = 2020,
            size_id              = 3
        )

        Apartment.objects.create(
            id                   = 23,
            price                = 5000,
            top_floor            = 22,
            floor                = 11,
            apartment_complex_id = 99,
            district_id          = 1,
            trade_type_id        = 2,
            trade_month          = 12,
            trade_year           = 2020,
            size_id              = 3
        )

    def tearDown(self):
        ApartmentComplex.objects.all().delete()
        Apartment.objects.all().delete()
        District.objects.all().delete()
        Neighborhood.objects.all().delete()
        TradeType.objects.all().delete()
        Size.objects.all().delete()

    def test_getting_apartments_graph_success(self):
        client   = Client()
        response = client.get('/apartment/graph/99?size_id=40')
        self.assertEquals(response.json(),
        {
            "trade_apartments_data": [
                {
                    "2019": [
                        {
                            "date": "2019. 6",
                            "values": [
                                6000,
                                1
                            ]
                        }
                    ]
                },
                {
                    "2020": [
                        {
                            "date": "2020. 11",
                            "values": [
                                7000,
                                1
                            ]
                        },
                        {
                            "date": "2020. 12",
                            "values": [
                                8000,
                                1
                            ]
                        }
                    ]
                }
            ],
            "rent_apartments_data": [
                {
                    "2019": [
                        {
                            "date": "2019. 3",
                            "values": [
                                3000,
                                1
                            ]
                        }
                    ]
                },
                {
                    "2020": [
                        {
                            "date": "2020. 11",
                            "values": [
                                4000,
                                1
                            ]
                        },
                        {
                            "date": "2020. 12",
                            "values": [
                                5000,
                                1
                            ]
                        }
                    ]
                }
            ]
        },
        )
        self.assertEqual(response.status_code, 200)

    def test_getting_apartments_graph_fail(self):
        client   = Client()
        response = client.get('/apartment/graph/99?size_id=555')
        self.assertEqual(response.json(),
        {
            "message":"INVALID_SIZE_ID"
        }
        )
        self.assertEqual(response.status_code, 400)

    def test_getting_apartments_graph_not_found(self):
        client   = Client()
        response = client.get('/apartment/50?complex=99')

class SearchTest(TestCase):

    maxDiff = None

    def setUp(self):
        client = Client()
        
        ApartmentComplex.objects.create(
            id               = 99,
            name             = '위코드아파트',
            household_number = 1234,
            completion_year  = 2020,
            address          = '서울시 위코드동',
            latitude         = str('37.518740000000001'),
            longitude        = str('127.020550000000001')
        )

        Neighborhood.objects.create(
            id        = 1,
            name      = "위코드구",
            latitude  = str('37.523433300000005'),
            longitude = str('127.024074900000006')
        )

    def tearDown(self):
        ApartmentComplex.objects.all().delete()
        Neighborhood.objects.all().delete()

    def test_getting_search_lists_success(self):
        client   = Client()
        response = client.get('/apartment/search?search=위코드')
        self.assertEquals(response.json(),{
            "lists": [
                {
                    "name"     : "위코드아파트",
                    "latitude" : str('37.518740000000001'),
                    "longitude": str('127.020550000000001'),
                    "address"  : "서울시 위코드동"
                },
                {
                    "name"     : "위코드구",
                    "latitude" : str('37.523433300000005'),
                    "longitude": str('127.024074900000006')
                }
            ]
        }
        )
        self.assertEqual(response.status_code, 200)

    def test_getting_search_lists_fail(self):
        client   = Client()
        response = client.get('/apartment/search?search=위코드2호점')
        self.assertEqual(response.json(),
        {
            "message":"NO_RESULT"
        }
        )
        self.assertEqual(response.status_code, 400)

    def test_getting_search_lists_not_found(self):
        client   = Client()
        response = client.get('/apartment/search/50')
        self.assertEqual(response.status_code, 404)

class ComplexDetailViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        Size.objects.create(
            id=1,
            area=84,
        )

        Size.objects.create(
            id=2,
            area=100,
        )

        TradeType.objects.create(
            id=1,
            name='전세',
        )

        TradeType.objects.create(
            id=2,
            name='매매',
        )

        District.objects.create(
            id=1,
            latitude=37.517295648357800,
            longitude=127.032660997667000,
        )

        Neighborhood.objects.create(
            id=1,
            latitude=37.492096371111000,
            longitude=127.073740857578000,
            district_id=1,
            name='위코드동'
        )

        ApartmentComplex.objects.create(
            id =1,
            name = '샤방샤방 아파트',
            household_number = 400,
            completion_year = 1995,
            address = '서울시 위코드구 위코드동',
            latitude = 37.492096371111000,
            longitude = 127.057477954524000,
            image_url='12345.jpg',
        )

        ApartmentComplex.objects.create(
            id = 2,
            name = '유코드  아파트',
            household_number = 1090,
            completion_year = 2020,
            address = '서울시 위코드구 위코드동',
            latitude = 37.492096852311000,
            longitude = 127.097477954524000,
            image_url = '12345.jpg',
        )

        Apartment.objects.create(
            price=1891000000.0000,
            top_floor=35,
            floor=8,
            trade_year=2012,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=1,
            size_id=1
        )

        Apartment.objects.create(
            price=1891000000.0000,
            top_floor=35,
            floor=8,
            trade_year=2015,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=1,
            size_id=1
        )

        Apartment.objects.create(
            price=91000000.0000,
            top_floor=18,
            floor=12,
            trade_year=2008,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=2,
            size_id=2,
        )

        Apartment.objects.create(
            price=91000000.0000,
            top_floor=18,
            floor=12,
            trade_year=2005,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=2,
            size_id=2,
        )

    def tearDown(self):
        Apartment.objects.all().delete()
        Size.objects.all().delete()
        TradeType.objects.all().delete()
        District.objects.all().delete()
        Neighborhood.objects.all().delete()
        ApartmentComplex.objects.all().delete()

    def test_complex_detail_view_success(self):
        client = Client()
        response = client.get('/apartment/complex/1')

        self.assertEquals(response.json(),{
            'complex': {
                'complex_id'      : 1,
                'complex_name'    : '샤방샤방 아파트',
                'completion_year' : '1995',
                'image_url'       : '12345.jpg',
                'household_number': 400,
                'address'         : '서울시 위코드구 위코드동',
                'size'            : [
                   {
                        'm^2'     : 84,
                        'p'       : 25,
                        'selling' : 1891000000.0000,
                        'renting' : 1891000000.0000,
                   },
                   {
                        'm^2'     : 100,
                        'p'       : 30,
                        'selling' : 91000000.0000,
                        'renting' : 91000000.0000,
                   }
               ],

                'trade_data'      : [
                   {
                        'trade_date' : '2015.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2012.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2008.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'p'          : 30,
                   },
                   {
                        'trade_date' : '2005.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'py'          : 30,
                   }
                ],
            }
        },
        )

        self.assertEqual(response.status_code, 200)

    def test_complex_detail_view_invalid_key(self):
        client = Client()
        response = client.get('/apartment/complex/')

        self.assertEquals(response.json(),{
            'complex': {
                'complex_id'      : 1,
                'complex_name'    : '샤방샤방 아파트',
                'completion_year' : '1995',
                'image_url'       : '12345.jpg',
                'household_number': 400,
                'address'         : '서울시 위코드구 위코드동',
                'size'            : [
                   {
                        'm^2'     : 84,
                        'p'       : 25,
                        'selling' : 1891000000.0000,
                        'renting' : 1891000000.0000,
                   },
                   {
                        'm^2'     : 100,
                        'p'       : 30,
                        'selling' : 91000000.0000,
                        'renting' : 91000000.0000,
                   }
               ],

                'trade_data'      : [
                   {
                        'trade_date' : '2015.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2012.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2008.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'p'          : 30,
                   },
                   {
                        'trade_date' : '2005.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'py'          : 30,
                   }
                ],
            }
        },
    )

        self.assertEqual(response.status_code, 400)


class ApartmentMapViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        Size.objects.create(
            id=1,
            area=95
        )

        TradeType.objects.create(
            id=1,
            name='매매',
        )

        District.objects.create(
            id=1,
            name='어디구',
            longitude=127.032660997667000,
            latitude=37.517295648357800,
        )

        Neighborhood.objects.create(
            id=1,
            name='무언동',
            longitude=127.046297922727000,
            latitude=37.493216740324100,
            distirict_id=1,
        )

        Apartment.objects.create(
            price=9936230000.0000,
            top_floor=100,
            floor=76,
            trade_year=2019,
            trade_month=12,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type=1,
            size_id=1
        )

        ApartmentComplex.objects.create(
            id=1,
            name='14기 아파트',
            household_number=200,
            completion_year=2020,
            image_url='fakeimage.jpg',
            address='서울시 어디구 무언동',
            longitude=37.519978100000000,
            latitude=127.059657200000000,
        )

        ApartmentComplex.objects.create(
            name='십사기 아파트',
            household_number=800,
            completion_year=2000,
            image_url='fakeimage2.jpg',
            address='서울시 어디구 무언동',
            longitude=37.5823978100000000,
            latitude=127.059857200000000,
        )

    def tearDown(self):
        ApartmentComplex.objects.all().delete()
        Apartment.objects.all().delete(),
        Neighborhood.objects.all().delete(),
        District.objects.all().delete(),
        TradeType.objects.all().delete(),
        Size.objects.all().delete(),

    def test_apartment_map_view_success(self):
        client = Client()
        response = client.get('/apartment/map?zoom_level=5&latitude=33.450701&longitude=126.570667&size1=1&size2=21')

        self.assertEquals(response.json(),
            {
                'result':
                    [
                        {
                            'neighborhood_id': 1,
                            'neighborhood_name': '무언동',
                            'latitude':37.493216740324100,
                            'longitude':127.046297922727000,
                            'average_price':9936230000.0000,
                        }
                    ]
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_apartment_map_view_not_found(self):
        client = Client()
        response = client.get('/apartment?zoom_level=5&latitude=33.450701&longitude=126.570667&size1=1&size2=21')
        self.assertEqual(response.status_code, 404)

class ComplexDetailViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        Size.objects.create(
            id=1,
            area=84,
        )

        Size.objects.create(
            id=2,
            area=100,
        )

        TradeType.objects.create(
            id=1,
            name='전세',
        )

        TradeType.objects.create(
            id=2,
            name='매매',
        )

        District.objects.create(
            id=1,
            latitude=37.517295648357800,
            longitude=127.032660997667000,
        )

        Neighborhood.objects.create(
            id=1,
            latitude=37.492096371111000,
            longitude=127.073740857578000,
            district_id=1,
            name='위코드동'
        )

        ApartmentComplex.objects.create(
            id =1,
            name = '샤방샤방 아파트',
            household_number = 400,
            completion_year = 1995,
            address = '서울시 위코드구 위코드동',
            latitude = 37.492096371111000,
            longitude = 127.057477954524000,
            image_url='12345.jpg',
        )

        ApartmentComplex.objects.create(
            id = 2,
            name = '유코드  아파트',
            household_number = 1090,
            completion_year = 2020,
            address = '서울시 위코드구 위코드동',
            latitude = 37.492096852311000,
            longitude = 127.097477954524000,
            image_url = '12345.jpg',
        )

        Apartment.objects.create(
            price=1891000000.0000,
            top_floor=35,
            floor=8,
            trade_year=2012,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=1,
            size_id=1
        )

        Apartment.objects.create(
            price=1891000000.0000,
            top_floor=35,
            floor=8,
            trade_year=2015,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=1,
            size_id=1
        )

        Apartment.objects.create(
            price=91000000.0000,
            top_floor=18,
            floor=12,
            trade_year=2008,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=2,
            size_id=2,
        )

        Apartment.objects.create(
            price=91000000.0000,
            top_floor=18,
            floor=12,
            trade_year=2005,
            trade_month=2,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type_id=2,
            size_id=2,
        )

    def tearDown(self):
        Apartment.objects.all().delete()
        Size.objects.all().delete()
        TradeType.objects.all().delete()
        District.objects.all().delete()
        Neighborhood.objects.all().delete()
        ApartmentComplex.objects.all().delete()

    def test_complex_detail_view_success(self):
        client = Client()
        response = client.get('/apartment/complex/1')

        self.assertEquals(response.json(),{
            'complex': {
                'complex_id'      : 1,
                'complex_name'    : '샤방샤방 아파트',
                'completion_year' : '1995',
                'image_url'       : '12345.jpg',
                'household_number': 400,
                'address'         : '서울시 위코드구 위코드동',
                'size'            : [
                   {
                        'm^2'     : 84,
                        'p'       : 25,
                        'selling' : 1891000000.0000,
                        'renting' : 1891000000.0000,
                   },
                   {
                        'm^2'     : 100,
                        'p'       : 30,
                        'selling' : 91000000.0000,
                        'renting' : 91000000.0000,
                   }
               ],

                'trade_data'      : [
                   {
                        'trade_date' : '2015.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2012.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2008.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'p'          : 30,
                   },
                   {
                        'trade_date' : '2005.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'py'          : 30,
                   }
                ],
            }
        },
        )

        self.assertEqual(response.status_code, 200)

    def test_complex_detail_view_invalid_key(self):
        client = Client()
        response = client.get('/apartment/complex/')

        self.assertEquals(response.json(),{
            'complex': {
                'complex_id'      : 1,
                'complex_name'    : '샤방샤방 아파트',
                'completion_year' : '1995',
                'image_url'       : '12345.jpg',
                'household_number': 400,
                'address'         : '서울시 위코드구 위코드동',
                'size'            : [
                   {
                        'm^2'     : 84,
                        'p'       : 25,
                        'selling' : 1891000000.0000,
                        'renting' : 1891000000.0000,
                   },
                   {
                        'm^2'     : 100,
                        'p'       : 30,
                        'selling' : 91000000.0000,
                        'renting' : 91000000.0000,
                   }
               ],

                'trade_data'      : [
                   {
                        'trade_date' : '2015.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2012.2',
                        'floor'      : 8,
                        'pricePerP'  : 74289285,
                        'trade_type' : '전세',
                        'm^2'        : 84,
                        'p'          : 25,
                   },
                   {
                        'trade_date' : '2008.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'p'          : 30,
                   },
                   {
                        'trade_date' : '2005.2',
                        'floor'      : 12,
                        'pricePerP'  : 3003000,
                        'trade_type' : '매매',
                        'm^2'        : 84,
                        'py'          : 30,
                   }
                ],
            }
        },
    )

        self.assertEqual(response.status_code, 400)


class ApartmentMapViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        Size.objects.create(
            id=1,
            area=95
        )

        TradeType.objects.create(
            id=1,
            name='매매',
        )

        District.objects.create(
            id=1,
            name='어디구',
            longitude=127.032660997667000,
            latitude=37.517295648357800,
        )

        Neighborhood.objects.create(
            id=1,
            name='무언동',
            longitude=127.046297922727000,
            latitude=37.493216740324100,
            distirict_id=1,
        )

        Apartment.objects.create(
            price=9936230000.0000,
            top_floor=100,
            floor=76,
            trade_year=2019,
            trade_month=12,
            apartment_complex_id=1,
            neighborhood_id=1,
            district_id=1,
            trade_type=1,
            size_id=1
        )

        ApartmentComplex.objects.create(
            id=1,
            name='14기 아파트',
            household_number=200,
            completion_year=2020,
            image_url='fakeimage.jpg',
            address='서울시 어디구 무언동',
            longitude=37.519978100000000,
            latitude=127.059657200000000,
        )

        ApartmentComplex.objects.create(
            name='십사기 아파트',
            household_number=800,
            completion_year=2000,
            image_url='fakeimage2.jpg',
            address='서울시 어디구 무언동',
            longitude=37.5823978100000000,
            latitude=127.059857200000000,
        )

    def tearDown(self):
        ApartmentComplex.objects.all().delete()
        Apartment.objects.all().delete(),
        Neighborhood.objects.all().delete(),
        District.objects.all().delete(),
        TradeType.objects.all().delete(),
        Size.objects.all().delete(),

    def test_apartment_map_view_success(self):
        client = Client()
        response = client.get('/apartment/map?zoom_level=5&latitude=33.450701&longitude=126.570667&size1=1&size2=21')

        self.assertEquals(response.json(),
            {
                'result':
                    [
                        {
                            'neighborhood_id': 1,
                            'neighborhood_name': '무언동',
                            'latitude':37.493216740324100,
                            'longitude':127.046297922727000,
                            'average_price':9936230000.0000,
                        }
                    ]
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_apartment_map_view_not_found(self):
        client = Client()
        response = client.get('/apartment?zoom_level=5&latitude=33.450701&longitude=126.570667&size1=1&size2=21')
        self.assertEqual(response.status_code, 404)
