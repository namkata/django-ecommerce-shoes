from AccountMgmt.serializers import ShoesTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenObtainSlidingView, TokenRefreshView


class ShoesTokenView(TokenObtainPairView):
    serializer_class = ShoesTokenObtainPairSerializer
