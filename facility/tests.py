from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock

from .models import School, Subway, ConvenientStore, Cafe, SchoolGrade, SubwayLine
from apartment.models import ApartmentComplex

class FacilityTest(TestCase):

    def setUp(self):
        client = Client()
        
        ApartmentComplex.objects.create(
            id               = 99,
            name             = 'wecode아파트',
            household_number = 1234,
            completion_year  = 2020,
            address          = '서울시 위코드동',
            latitude         = 37.518740000000001,
            longitude        = 127.020550000000001
        )

        ApartmentComplex.objects.create(
            id               = 98,
            name             = 'wecode아파트2',
            household_number = 1234,
            completion_year  = 2020,
            address          = '서울시 위코드동',
            latitude         = 137.518740000000001,
            longitude        = 1127.020550000000001
        )

        SchoolGrade.objects.create(
            id    = 1,
            grade = '초'
        )

        School.objects.create(
            id              = 1,
            name            = '위코드초등학교',
            latitude        = str('37.523433300000005'),
            longitude       = str('127.024074900000006'),
            school_grade_id = 1
        )

        SubwayLine.objects.create(
            id   = 1,
            line = '위코드라인'
        )

        Subway.objects.create(
            id             = 1,
            name           = '위코드역',
            latitude       = str('37.523433300000005'),
            longitude      = str('127.024074900000006'),
            subway_line_id = 1
        )

        ConvenientStore.objects.create(
            id        = 1,
            name      = '위코드CU',
            latitude  = str('37.523433300000005'),
            longitude = str('127.024074900000006')
        )

        Cafe.objects.create(
            id        = 1,
            name      = '위코드스타벅스',
            latitude  = str('37.523433300000005'),
            longitude = str('127.024074900000006')
        )

    def tearDown(self):
        School.objects.all().delete()
        Subway.objects.all().delete()
        ConvenientStore.objects.all().delete()
        Cafe.objects.all().delete()

    def test_getting_near_facilities_success(self):
        client   = Client()
        response = client.get('/facility/99')

        self.assertEquals(response.json(),
        {
            "school": [
                {
                    "id"       : 1,
                    "name"     : "위코드초등학교",
                    "latitude" : str('37.523433300000005'),
                    "longitude": str('127.024074900000006'),
                    "distance" : 607
                }
            ],
            "subway": [
                {
                    "id"       : 1,
                    "name"     : "위코드역",
                    "latitude" : str('37.523433300000005'),
                    "longitude": str('127.024074900000006'),
                    "distance" : 607
                }
            ],
            "convenient_store": [
                {
                    "id"       : 1,
                    "name"     : "위코드CU",
                    "latitude" : str('37.523433300000005'),
                    "longitude": str('127.024074900000006'),
                    "distance" : 607
                }
            ],
            "cafe": [
                {
                    "id"       : 1,
                    "name"     : "위코드스타벅스",
                    "latitude" : str('37.523433300000005'),
                    "longitude": str('127.024074900000006'),
                    "distance" : 607
                }
            ]
        }
        )
        self.assertEqual(response.status_code, 200)

    def test_getting_near_facilities_fail(self):
        client   = Client()
        response = client.get('/facility/98')
        self.assertEqual(response.json(),
        {
            "message":"INVALID_COORDINATE"
        }
        )
        self.assertEqual(response.status_code, 400)

    def test_getting_near_facilities_not_found(self):
        client   = Client()
        response = client.get('/facility?complex=99')
        self.assertEqual(response.status_code, 404)
