from django.urls import include, path

urlpatterns = [
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/access/", include("apps.access.urls")),
    path("api/business/", include("apps.business.urls")),
]
