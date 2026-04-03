from django.urls import path

from apps.business.views import ProductDetailView, ProductsView

urlpatterns = [
    path("products/", ProductsView.as_view()),
    path("products/<int:product_id>/", ProductDetailView.as_view()),
]
