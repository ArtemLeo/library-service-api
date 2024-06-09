from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)
from telegram_api.telegram_helper import telegram_helper


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["retrieve", "return_borrowing"]:
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        return self.filter_queryset(self.queryset)

    def filter_queryset(self, queryset):
        current_user = self.request.user
        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        if not current_user.is_staff:
            queryset = queryset.filter(user=current_user)
        else:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        return queryset

    @staticmethod
    def notify_borrowing(borrowing):
        message = (
            f"📚 *New Borrowing Created* \n\n"
            f"*Borrowing ID:*   {borrowing.pk}\n"
            f"*Borrowing Date:*   {borrowing.borrow_date}\n"
            f"*Expected Return Date:*   {borrowing.expected_return_date}\n"
            f"*Book Title:*   {borrowing.book.title}\n"
            f"*Book Author:*   {borrowing.book.author}"
        )
        telegram_helper.send_message(message)

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        self.notify_borrowing(borrowing)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def return_borrowing(self, request, pk=None):
        """
        Endpoint for marking a borrowing as
        returned by providing the actual return date
        """
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by actual return date (ex. ?is_active=True)",
            ),
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description="Filter by user id (ex. ?user_id=2)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
