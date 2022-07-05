from AccountMgmt.models import StoreLogin
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSlidingSerializer


class ShoesTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["expire_at"] = token.current_time + settings.REFRESH_LIFE_TIME
        return token

    def validate(self, attrs):
        param_invocation_id = self.context.get("invocation_id")
        param_gmd_session = self.context.get("gmd_session")
        data = super().validate(attrs)
        store_login = StoreLogin.objects.filter(
            account_id=self.user.id, invocation_id=param_invocation_id, gmd_session=param_gmd_session
        ).first()

        if not store_login:
            store_login = StoreLogin.objects.create(
                invocation_id=param_invocation_id, gmd_session=param_gmd_session, account_id=self.user.id
            )
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
