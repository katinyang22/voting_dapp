from datetime import timedelta
from django.conf import settings
from rest_framework import generics, views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_user_totp_device
from .permissions import IsOtpVerified
from .serializers import TOTPCustomTokenObtainPairSerializer, TOTPCustomTokenRefreshSerialzier, UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenRefreshView

# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = RefreshToken.for_user(user=user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "refresh": token.__str__(),
      "access": token.access_token.__str__()
    })

class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]    
    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)

class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]    
    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            token = TOTPCustomTokenObtainPairSerializer().get_token(user=user)
            token.set_exp(lifetime=timedelta(hours=settings.CUSTOM_AUTH_VALUES['REFRESH_TOKEN_LIFETIME']))
            access_token = token.access_token
            access_token.set_exp(lifetime=timedelta(hours=settings.CUSTOM_AUTH_VALUES['ACCESS_TOKEN_LIFETIME']))
            return Response({'refresh': token.__str__(), 'access': access_token.__str__()}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class TOTPCustomTokenRefreshView(TokenRefreshView):
    serializer_class = TOTPCustomTokenRefreshSerialzier

# Get User API
class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated, IsOtpVerified
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user
