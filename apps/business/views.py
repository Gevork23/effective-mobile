from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access.services import AccessService
from apps.core.permissions import IsAuthenticatedCustom

MOCK_PRODUCTS = [
    {"id": 1, "name": "Ноутбук", "owner_id": "11111111-1111-1111-1111-111111111111"},
    {"id": 2, "name": "Мышь", "owner_id": "22222222-2222-2222-2222-222222222222"},
]


class ProductsView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        if not AccessService.has_permission(request.user, "products", "read"):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return Response(MOCK_PRODUCTS)

    def post(self, request):
        if not AccessService.has_permission(request.user, "products", "create"):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Продукт создан (mock)"}, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def patch(self, request, product_id: int):
        product = next((item for item in MOCK_PRODUCTS if item["id"] == product_id), None)
        if not product:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        if not AccessService.has_permission(request.user, "products", "update", owner_id=product["owner_id"]):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Продукт обновлен (mock)"})

    def delete(self, request, product_id: int):
        product = next((item for item in MOCK_PRODUCTS if item["id"] == product_id), None)
        if not product:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        if not AccessService.has_permission(request.user, "products", "delete", owner_id=product["owner_id"]):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Продукт удален (mock)"}, status=status.HTTP_200_OK)
