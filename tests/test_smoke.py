import unittest
from uuid import uuid4
from datetime import date

from fastapi.testclient import TestClient

from app import app


class SmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

        # unique user per test run to avoid conflicts with existing DB rows
        uid = uuid4().hex[:8]
        cls.username = f"testuser_{uid}"
        cls.email = f"{cls.username}@example.com"
        cls.password = "secret123"

        # register
        r = cls.client.post("/api/v1/auth/register", json={
            "username": cls.username,
            "email": cls.email,
            "password": cls.password,
        })
        assert r.status_code in (200, 201)

        # login (form encoded)
        r = cls.client.post(
            "/api/v1/auth/login",
            data={"username": cls.username, "password": cls.password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert r.status_code == 200
        token = r.json().get("access_token")
        assert token
        cls.auth_headers = {"Authorization": f"Bearer {token}"}

    def test_author_and_book_and_borrow_flow(self):
        # Create an author
        payload = {"name": "Test Author", "bio": "Bio"}
        r = self.client.post("/api/v1/authors/", json=payload, headers=self.auth_headers)
        self.assertIn(r.status_code, (200, 201))
        author = r.json()
        self.assertIn("id", author)
        author_id = author["id"]

        # List authors (ensure our author appears)
        r = self.client.get("/api/v1/authors/", headers=self.auth_headers)
        self.assertEqual(r.status_code, 200)
        authors = r.json()
        self.assertTrue(any(a.get("id") == author_id for a in authors))

        # Create a book
        book_payload = {
            "title": "Test Book",
            "author_id": author_id,
            "publication_date": str(date.today()),
        }
        r = self.client.post("/api/v1/books/", json=book_payload, headers=self.auth_headers)
        self.assertIn(r.status_code, (200, 201))
        book = r.json()
        self.assertIn("id", book)
        book_id = book["id"]

        # Get book
        r = self.client.get(f"/api/v1/books/{book_id}", headers=self.auth_headers)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("id"), book_id)

        # Borrow book
        r = self.client.post("/api/v1/borrow/", json={"book_id": book_id, "days": 7}, headers=self.auth_headers)
        self.assertIn(r.status_code, (200, 201))
        borrow = r.json()
        self.assertIn("id", borrow)
        record_id = borrow["id"]

        # Attempt to borrow again should fail (409)
        r = self.client.post("/api/v1/borrow/", json={"book_id": book_id, "days": 7}, headers=self.auth_headers)
        self.assertIn(r.status_code, (409,))

        # Return book
        r = self.client.post(f"/api/v1/borrow/return/{record_id}", headers=self.auth_headers)
        self.assertEqual(r.status_code, 200)
        returned = r.json()
        self.assertIsNotNone(returned.get("returned_at"))


if __name__ == "__main__":
    unittest.main()
