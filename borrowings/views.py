from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def get_queryset(self):
        return self.filter_queryset(self.queryset)

    def filter_queryset(self, queryset):
        current_user = self.request.user
        if not current_user.is_staff:
            queryset = queryset.filter(user=current_user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
