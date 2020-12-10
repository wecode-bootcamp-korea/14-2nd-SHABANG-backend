
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
            neighborhood_id = 1
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
            size_id              = 40
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
            size_id              = 40
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
            size_id              = 40
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
            size_id              = 40
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
            size_id              = 40
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
            size_id              = 40
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
