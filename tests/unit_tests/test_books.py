"""
Unit tests for the Book endpoints and business logic
Run with: pytest tests/test_books.py -v
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app


# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture
def sample_book():
    """Sample book data"""
    return {"id": 1, "title": "Test Book", "author": "Test Author", "created_at": "2024-01-01T00:00:00"}


# ------------------------------
# Override database dependency
# ------------------------------
def get_mock_connection():
    """Override for database connection dependency"""
    conn = Mock()
    conn.commit = Mock()
    conn.rollback = Mock()
    conn.cursor = Mock()
    yield conn


# ------------------------------
# Test Client Setup
# ------------------------------
@pytest.fixture
def client():
    """Create test client with mocked database"""
    from app.database.core import get_connection
    app.dependency_overrides[get_connection] = get_mock_connection
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ------------------------------
# Book Endpoint Tests
# ------------------------------
class TestBookEndpoints:

    @patch('app.bizlogic.books.list_books')
    def test_list_books_success(self, mock_list_books, client, sample_book):
        """Test GET /books returns list of books"""
        mock_list_books.return_value = [sample_book]

        response = client.get("/books")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["title"] == "Test Book"

    @patch('app.bizlogic.books.get_book')
    def test_get_book_success(self, mock_get_book, client, sample_book):
        """Test GET /books/{book_id} returns book"""
        mock_get_book.return_value = sample_book

        response = client.get("/books/1")

        assert response.status_code == 200
        assert response.json()["title"] == "Test Book"

    @patch('app.bizlogic.books.get_book')
    def test_get_book_not_found(self, mock_get_book, client):
        """Test GET /books/{book_id} returns 404 when book not found"""
        mock_get_book.return_value = None

        response = client.get("/books/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"

    @patch('app.bizlogic.books.insert_book')
    def test_create_book_success(self, mock_insert_book, client):
        """Test POST /books creates new book"""
        mock_insert_book.return_value = {
            "id": 1,
            "title": "New Book",
            "author": "New Author"
        }

        response = client.post("/books", json={
            "title": "New Book",
            "author": "New Author"
        })

        assert response.status_code == 200
        assert response.json()["title"] == "New Book"

    def test_create_book_invalid_data(self, client):
        """Test POST /books with invalid data returns 422"""
        response = client.post("/books", json={"invalid": "field"})

        assert response.status_code == 422

    def test_create_book_missing_title(self, client):
        """Test POST /books with missing title returns 422"""
        response = client.post("/books", json={"author": "Author Only"})

        assert response.status_code == 422

    def test_create_book_missing_author(self, client):
        """Test POST /books with missing author returns 422"""
        response = client.post("/books", json={"title": "Title Only"})

        assert response.status_code == 422


# ------------------------------
# Book Business Logic Tests
# ------------------------------
class TestBookBusinessLogic:

    @patch('app.bizlogic.books.insert_book')
    def test_insert_book_commits_transaction(self, mock_insert_book):
        """Test that insert_book commits the transaction"""
        from app.bizlogic.books import insert_book

        mock_conn = Mock()
        mock_insert_book.return_value = {"id": 1, "title": "New Book", "author": "Author"}

        result = insert_book(mock_conn, title="New Book", author="Author")

        assert result["title"] == "New Book"
        mock_insert_book.assert_called_once_with(mock_conn, title="New Book", author="Author")

    @patch('app.bizlogic.books.get_book')
    def test_get_book_returns_book(self, mock_get_book):
        """Test that get_book returns book data"""
        from app.bizlogic.books import get_book

        mock_conn = Mock()
        mock_get_book.return_value = {"id": 1, "title": "Test Book"}

        result = get_book(mock_conn, 1)

        assert result["title"] == "Test Book"

    @patch('app.bizlogic.books.list_books')
    def test_list_books_returns_list(self, mock_list_books):
        """Test that list_books returns list of books"""
        from app.bizlogic.books import list_books

        mock_conn = Mock()
        mock_list_books.return_value = [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"}
        ]

        result = list_books(mock_conn)

        assert len(result) == 2
        assert result[0]["title"] == "Book 1"
        mock_list_books.assert_called_once_with(mock_conn)
