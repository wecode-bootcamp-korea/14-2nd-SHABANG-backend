from unittest.mock  import patch, MagicMock

from django.test import TestCase, Client

from .models import User, Platform

class KakaoLogInTest(TestCase):
    def setUp(self):
        Platform.objects.create(
            id=1,
            name='카카오'
        )
        User.objects.create(
            name ='test',
            email='test@wecode.com',
            phone_number='01011111111',
            platform_id=1
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_kakao_login_view_post_success(self, mocked_request):
        class Response:
            def json(self):
                return {
                        'kakao_account' : {
                            'profile'     : {'nickname':'test'},
                            'email'       : 'test@wecode.com',
                        }
                }

        mocked_request.get = MagicMock(return_value=Response())
        headers = {'HTTP_AUTHORIZATION':'TOKEN'}
        response = self.client.post('/user/kakaologin', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
#
    @patch('user.views.requests')
    def test_kakao_login_view_post_invalid_key(self, mocked_request):
        class Response:
            def json(self):
                return {
                        'kakao_account' : {
                            'profile'     : {'nickname':'kakao'},
                        }
                }

        mocked_request.get = MagicMock(return_value=Response())

        headers = {'Authorization':'ACCESS_TOKEN'}
        response = self.client.post('/user/kakaologin', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 400)

class GoogleLogInTest(TestCase):
    def setUp(self):
        Platform.objects.create(
            id=2,
            name='구글'
        )

        User.objects.create(
            name ='test',
            email='test@wecode.com',
            phone_number='01011111111',
            platform_id=2
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_google_login_view_post_success(self, mocked_request):
        class Response:
            def json(self):
                return {
                        'name' : 'google',
                        'email': 'google@wecode.com',
                }
        mocked_request.get = MagicMock(return_value=Response())

        headers = {'HTTP_Authorization':'ACCESS_TOKEN'}
        response = self.client.post('/user/googlelogin', **headers, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_google_login_view_post_invalid_key(self, mocked_request):
        class Response:
            def json(self):
                return {
                        'name' : 'google',
                    }

        mocked_request.get = MagicMock(return_value=Response())

        headers = {'Authorization':'ACCESS_TOKEN'}
        response = self.client.post('/user/googlelogin', **headers, content_type='application/json')

        self.assertEqual(response.status_code, 400)
