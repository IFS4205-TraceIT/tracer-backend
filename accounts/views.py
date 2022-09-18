from typing import Any, Optional

from django.conf import settings
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import AuthUser
from infections.models import Contacttracers
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegistrationSerializer,
    UserSerializer,
    RegisterTOTPSerializer,
    ValidateTOTPSerializer
)
from .vault import create_vault_client
from .vault.totp import TOTP


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        """Return user response after a successful registration."""
        user_request = request.data
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ct = Contacttracers(id=serializer.data['id'])
        ct.save()
        del serializer.data['id']
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        try:
            Contacttracers.objects.get(id=serializer.data['id'])
        except Contacttracers.DoesNotExist:
            return Response(data={'user':{'error':['Invalid User']}}, status=status.HTTP_400_BAD_REQUEST)

        del serializer.data['id']
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
        """Return user on GET request."""
        serializer = self.serializer_class(request.user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
        """Return updated user."""
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterTOTPView(APIView):
    serializer_class = RegisterTOTPSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(request.user, data={'has_otp': True}, context={'request': request})
        serializer.is_valid(raise_exception=True)

        vault = create_vault_client()
        totp = TOTP(vault)

        img = totp.create_key(generate=True, name=request.user.id, issuer='TraceIT', account_name=request.user.username)

        serializer.save()

        return Response(img['data'], status=status.HTTP_200_OK)


class ValidateTOTPView(TokenObtainPairView):
    serializer_class = ValidateTOTPSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
