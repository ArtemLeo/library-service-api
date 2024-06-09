from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from datetime import timedelta

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(borrow_date__gte=timezone.now().date()),
                name="borrow_date_not_past",
            ),
            models.CheckConstraint(
                check=(
                        Q(expected_return_date__gte=F("borrow_date"))
                        & Q(actual_return_date__gte=F("borrow_date"))
                ),
                name="return_date_gte_borrow_date",
            ),
            models.CheckConstraint(
                check=Q(
                    expected_return_date__lte=(
                            F("borrow_date") + timedelta(weeks=2)
                    )
                ),
                name="expected_return_date_within_two_weeks",
            ),
        ]

    @staticmethod
    def validate_inventory(book, error_to_raise):
        if book.inventory <= 0:
            raise error_to_raise(
                {
                    "book": f"All copies of the '{book.title}' "
                            f"are currently unavailable for borrowing."
                }
            )

    def clean(self):
        Borrowing.validate_inventory(
            self.book,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
            **kwargs
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.book} borrowed by {self.user}"
