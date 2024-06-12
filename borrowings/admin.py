from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "borrow_date",
        "actual_return_date",
        "book",
        "user",
    )
    search_fields = ("id", "user__email", "book__title")
    ordering = (
        "-borrow_date",
        "actual_return_date",
    )
