from AccountMgmt.models import Account, HistoryAccessToken, HistoryRefreshToken, StoreLogin
from django.contrib import admin

# Register your models here.

admin.site.register(Account)
admin.site.register(StoreLogin)
admin.site.register(HistoryRefreshToken)
admin.site.register(HistoryAccessToken)
