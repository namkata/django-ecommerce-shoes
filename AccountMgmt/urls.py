from AccountMgmt import views
from django.urls import path

urlpatterns = [
    path("signin/", views.ShoesTokenView.as_view(), name="login"),
    path("renewal-token/", views.ShoesRefreshToken.as_view(), name="renewal"),
]
