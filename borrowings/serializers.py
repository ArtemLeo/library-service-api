from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = fields

    def validate(self, attrs):
        data = super(BorrowingDetailSerializer, self).validate(attrs=attrs)

        if self.instance.actual_return_date:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.actual_return_date = datetime.now().date()
        instance.save()

        book = instance.book
        book.inventory += 1
        book.save()

        return instance


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        )

    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs=attrs)
        Borrowing.validate_inventory(attrs["book"], ValidationError)
        return data

    @transaction.atomic
    def create(self, validated_data):
        borrowing = Borrowing.objects.create(**validated_data)
        book = validated_data.get("book")
        book.inventory -= 1
        book.save()
        return borrowing
