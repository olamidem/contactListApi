import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    # override method call authenticate
    def authenticate(self, request):
        # get the header
        auth_data = authentication.get_authorization_header(request)
        # check if user is not supplying auth auth_data
        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        # validate the token
        try:
            # auth_token = jwt.encode({'username': User.username}, settings.JWT_SECRET_KEY, algorithm="HS256")
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
        
            # payload = jwt.decode(token, settings.JWT_SECRET_KEY)

            user = User.objects.get(username=payload['username'])
            return user, token

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Your token is invalid, login')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Your token is expired, login')

        return super().authenticate(request)
