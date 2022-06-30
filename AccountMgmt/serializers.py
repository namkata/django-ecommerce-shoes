from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSlidingSerializer


class ShoesTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        result = {
            "message": "Success",
            "data": {
                "userName": self.user.username,
                "fullName": self.user.get_full_name(),
                "phone": self.user.phone[:3] + "x" * 5 + self.user.phone[9:],
                "refresh": data["refresh"],
                "access": data["access"],
            },
        }
        return result
