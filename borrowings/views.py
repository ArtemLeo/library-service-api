from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer
