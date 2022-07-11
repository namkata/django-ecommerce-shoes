from datetime import datetime

from AccountMgmt.models import Account, HistoryAccessToken, HistoryRefreshToken, StoreLogin
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework_simplejwt.tokens import AccessToken


class AccountAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:
        Authorization: Bearer ...token...
    """

    keyword = "Bearer"
    model = Account

    def get_model(self):
        if self.model is not None:
            return self.model
        return Account

    def authenticate(self, request):
        auth_header_value = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header_value:
            raise exceptions.PermissionDenied()
        if "Bearer" not in auth_header_value:
            raise exceptions.PermissionDenied()

        access_token = auth_header_value.replace("Bearer ", "")

        # access_token = self.get_validated_token(access_token)
        return self.authenticate_credentials(
            access_token, request.META.get("INVOCATION_ID"), request.META.get("GDMSESSION")
        )

    def authenticate_credentials(self, access_token, invocation_id, gmdsession):
        try:
            access = HistoryAccessToken.objects.get(access_token=access_token)
        except HistoryAccessToken.DoesNotExist:
            raise exceptions.AuthenticationFailed()
        verify = AccessToken(access_token).verify

        if not verify:
            raise exceptions.AuthenticationFailed(_("Token is expired"))

        return access.refresh.store.account, access_token

    def authenticate_header(self, request):
        return self.keyword
