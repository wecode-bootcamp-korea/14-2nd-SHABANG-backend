import json, jwt, requests

from django.views import View
from django.http  import JsonResponse

from .models      import User
from core.my_settings import SECRET, ALGORITHM

class KakaoLogInView(View):
    def post(self, request):
        try:
            ACCESS_TOKEN  = request.headers['Authorization']
            kakao_json    = requests.get('https://kapi.kakao.com/v2/user/me', headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"})
            kakao_profile = kakao_json.json().get('kakao_account')

            user_name  = kakao_profile['profile']['nickname']
            user_email = kakao_profile['email']

            if User.objects.filter(name=user_name, email=user_email, platform_id=1).exists():
                user         = User.objects.get(name=user_name, email=user_email, platform_id=1)
                access_token = jwt.encode({'id':user.id}, SECRET['secret'], algorithm=ALGORITHM['algorithm']).decode('utf-8')

                return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

            User.objects.create(name=user_name, email=user_email, platform_id=1)

            user         = User.objects.get(name=user_name, email=user_email, platform_id=1)
            access_token = jwt.encode({'id':user.id}, SECRET['secret'], algorithm=ALGORITHM['algorithm']).decode('utf-8')

            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 

class GoogleLogInView(View):
    def post(self, request):
        try:
            ACCESS_TOKEN   = request.headers['Authorization']
            google_json    = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={ACCESS_TOKEN}')
            google_profile = google_json.json()

            user_name = google_profile['name']
            user_email = google_profile['email']

            if User.objects.filter(name=user_name, email=user_email, platform_id=2).exists():
                user = User.objects.get(name=user_name, email=user_email, platform_id=2)
                access_token = jwt.encode({'id':user.id}, SECRET['secret'], algorithm=ALGORITHM['algorithm']).decode('utf-8')

                return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

            User.objects.create(name=user_name, email=user_email, platform_id=2)

            user = User.objects.get(name=user_name, email=user_email, platform_id=2)
            access_token = jwt.encode({'id':user.id}, SECRET['secret'], algorithm=ALGORITHM['algorithm']).decode('utf-8')

            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

def login_decorator(func):
    def inner(self, request, *args, **kwargs):
        try:
            auth_token   = request.headers.get('Authorization', None)
            payload      = jwt.decode(auth_token, SECRET['secret'], algorithm=ALGORITHM['algorithm'])
            user         = User.objects.get(id=payload['id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

    return inner
