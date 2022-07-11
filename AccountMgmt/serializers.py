from AccountMgmt.models import HistoryAccessToken, HistoryRefreshToken, StoreLogin
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSlidingSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class ShoesTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        param_invocation_id = self.context.get("invocation_id")
        param_gmd_session = self.context.get("gmd_session")
        store_sign = StoreLogin.objects.filter(
            invocation_id=param_invocation_id, gmd_session=param_gmd_session, account_id=self.user.id
        ).first()
        if not store_sign:
            store_login = StoreLogin.objects.create(
                invocation_id=param_invocation_id, gmd_session=param_gmd_session, account_id=self.user.id
            )
            res = super().get_token(user)
            refresh = HistoryRefreshToken.objects.create(store=store_login, refresh_token=res)
            HistoryAccessToken.objects.create(refresh=refresh, access_token=res.access_token)
            return res

        refresh = HistoryRefreshToken.objects.get(store=store_sign)
        access = HistoryAccessToken.objects.filter(refresh=refresh).last()
        if refresh.is_expired:
            res = RefreshToken().for_user(user)
            refresh.refresh_token = res
            refresh.save()
            access.access_token = res.access_token
            access.save()
            return res

        res = self.token_class(refresh.refresh_token)
        access.access_token = res.access_token
        access.save()
        return res

    def validate(self, attrs):
        data = super().validate(attrs)

        fullName = "Unknown"
        if self.user.get_full_name():
            fullName = self.user.get_full_name()

        phone = "Unknown"
        if self.user.phone:
            phone = self.user.phone[:3] + "*" * 5 + self.user.phone[-4:]
        result = {
            "message": "Success",
            "data": {
                "userName": self.user.username,
                "fullName": fullName,
                "phone": phone,
                "refresh": data["refresh"],
                "access": data["access"],
            },
        }
        return result
