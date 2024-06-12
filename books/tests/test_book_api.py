from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse("book:book-list")


def sample_book(**params):
    defaults = {
        "title": "BookTitle",
        "author": "BookAuthor",
        "cover": 1,
        "inventory": 1,
        "daily_fee": 2.55
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def detail_url(book_id: int):
    return reverse("book:book-detail", args=[book_id])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_books(self):
        sample_book()
        sample_book()

        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "BookTitle",
            "author": "BookAuthor",
            "cover": 1,
            "inventory": 1,
            "daily_fee": 2.55
        }

        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_forbidden(self):
        book = sample_book()
        book_url = detail_url(book.id)

        payload = {
            "id": book.id,
            "title": "BookTitle",
            "author": "BookAuthor",
            "cover": 1,
            "inventory": 1,
            "daily_fee": 2.55
        }

        res = self.client.put(book_url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_forbidden(self):
        book = sample_book()
        book_url = detail_url(book.id)

        res = self.client.delete(book_url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "BookTitle",
            "author": "BookAuthor",
            "cover": 1,
            "inventory": 1,
            "daily_fee": 2.55
        }

        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        book = sample_book()
        book_url = detail_url(book.id)

        payload = {
            "id": book.id,
            "title": "BookTitle",
            "author": "BookAuthor",
            "cover": 1,
            "inventory": 1,
            "daily_fee": 2.55
        }

        res = self.client.put(book_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        book = sample_book()
        book_url = detail_url(book.id)

        res = self.client.delete(book_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
