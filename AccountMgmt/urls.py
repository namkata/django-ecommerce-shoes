from AccountMgmt import views
from django.urls import path

urlpatterns = [path("token/", views.ShoesTokenView.as_view(), name="token")]
