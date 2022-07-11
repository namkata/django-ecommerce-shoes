from AccountMgmt.serializers import ShoesTokenObtainPairSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ShoesTokenView(TokenObtainPairView):
    serializer_class = ShoesTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data,
            context={"invocation_id": request.META.get("INVOCATION_ID"), "gmd_session": request.META.get("GDMSESSION")},
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ShoesRefreshToken(TokenRefreshView):
    pass
