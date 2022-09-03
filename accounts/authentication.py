from rest_framework_simplejwt.authentication import JWTAuthentication

class TwoFactorAuthentication(JWTAuthentication):
    def authenticate(self, request):
        values = super().authenticate(request)
        if values is None:
            return None
        
        if values[0] is None or values[1] is None:
            return None

        user, validated_token = values
        if ('verified_otp' not in validated_token) or (not validated_token['verified_otp']):
            return None

        return user, validated_token