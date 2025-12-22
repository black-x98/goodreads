"""
Unit tests for the Goodreads Clone API
Run with: pytest tests/test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app


# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture
def mock_db_connection():
    """Mock database connection"""
    conn = Mock()
    conn.commit = Mock()
    conn.rollback = Mock()
    conn.cursor = Mock()
    return conn


@pytest.fixture
def sample_user():
    """Sample user data"""
    return {"id": 1, "name": "Alice", "created_at": "2024-01-01T00:00:00"}


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
# User Endpoint Tests
# ------------------------------
class TestUserEndpoints:

    @patch('app.bizlogic.users.list_users_query')
    def test_list_users_success(self, mock_list_query, client, sample_user):
        """Test GET /users returns list of users"""
        mock_list_query.return_value = [sample_user]

        response = client.get("/users")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Alice"
        mock_list_query.assert_called_once()

    @patch('app.bizlogic.users.get_user_query')
    def test_get_user_success(self, mock_get_query, client, sample_user):
        """Test GET /users/{user_id} returns user"""
        mock_get_query.return_value = sample_user

        response = client.get("/users/1")

        assert response.status_code == 200
        assert response.json()["name"] == "Alice"
        assert response.json()["id"] == 1

    @patch('app.bizlogic.users.get_user_query')
    def test_get_user_not_found(self, mock_get_query, client):
        """Test GET /users/{user_id} returns 404 when user not found"""
        mock_get_query.return_value = None

        response = client.get("/users/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    @patch('app.bizlogic.users.insert_user_query')
    def test_create_user_success(self, mock_insert_query, client, sample_user):
        """Test POST /users creates new user"""
        mock_insert_query.return_value = sample_user

        response = client.post("/users", json={"name": "Alice"})

        assert response.status_code == 200
        assert response.json()["name"] == "Alice"
        mock_insert_query.assert_called_once()

    def test_create_user_invalid_data(self, client):
        """Test POST /users with invalid data returns 422"""
        response = client.post("/users", json={"invalid": "field"})

        assert response.status_code == 422

    def test_create_user_missing_name(self, client):
        """Test POST /users with missing name returns 422"""
        response = client.post("/users", json={})

        assert response.status_code == 422


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


# ------------------------------
# Review Endpoint Tests
# ------------------------------
class TestReviewEndpoints:

    @patch('app.bizlogic.reviews.add_review')
    def test_add_review_success(self, mock_add_review, client):
        """Test POST /reviews creates new review"""
        mock_add_review.return_value = {
            "id": 1,
            "user_id": 1,
            "book_id": 1,
            "rating": 5,
            "content": "Great book!"
        }

        response = client.post("/reviews", json={
            "user_id": 1,
            "book_id": 1,
            "rating": 5,
            "content": "Great book!"
        })

        assert response.status_code == 200
        assert response.json()["rating"] == 5
        assert response.json()["content"] == "Great book!"

    @patch('app.bizlogic.reviews.list_reviews_by_user')
    def test_list_reviews_by_user(self, mock_list_reviews, client):
        """Test GET /users/{user_id}/reviews returns user reviews"""
        mock_list_reviews.return_value = [
            {"id": 1, "rating": 5, "content": "Great!"},
            {"id": 2, "rating": 4, "content": "Good!"}
        ]

        response = client.get("/users/1/reviews")

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["rating"] == 5

    @patch('app.bizlogic.reviews.list_reviews_by_book')
    def test_list_reviews_by_book(self, mock_list_reviews, client):
        """Test GET /books/{book_id}/reviews returns book reviews"""
        mock_list_reviews.return_value = [
            {"id": 1, "user_id": 1, "rating": 5}
        ]

        response = client.get("/books/1/reviews")

        assert response.status_code == 200
        assert len(response.json()) == 1


# ------------------------------
# Follow Endpoint Tests
# ------------------------------
class TestFollowEndpoints:

    @patch('app.bizlogic.follows.follow_user')
    def test_follow_user_success(self, mock_follow, client):
        """Test POST /follow/{followee_id} creates follow relationship"""
        mock_follow.return_value = {"follower_id": 1, "followee_id": 2}

        response = client.post("/follow/2?follower_id=1")

        assert response.status_code == 200
        assert response.json()["followee_id"] == 2

    @patch('app.bizlogic.follows.unfollow_user')
    def test_unfollow_user_success(self, mock_unfollow, client):
        """Test POST /unfollow/{followee_id} removes follow relationship"""
        mock_unfollow.return_value = None

        response = client.post("/unfollow/2?follower_id=1")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @patch('app.bizlogic.follows.get_newsfeed')
    def test_get_newsfeed(self, mock_newsfeed, client):
        """Test GET /users/{user_id}/newsfeed returns feed"""
        mock_newsfeed.return_value = [
            {
                "user_name": "Bob",
                "book_title": "Great Book",
                "rating": 5,
                "content": "Loved it!"
            }
        ]

        response = client.get("/users/1/newsfeed")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["user_name"] == "Bob"


# ------------------------------
# Business Logic Tests
# ------------------------------
class TestUserBusinessLogic:

    @patch('app.bizlogic.users.insert_user_query')
    def test_insert_user_commits_transaction(self, mock_insert_query):
        """Test that insert_user commits the transaction"""
        from app.bizlogic.users import insert_user

        mock_conn = Mock()
        mock_insert_query.return_value = {"id": 1, "name": "Alice"}

        result = insert_user(mock_conn, name="Alice")

        assert result["name"] == "Alice"
        mock_insert_query.assert_called_once_with(mock_conn, name="Alice")
        mock_conn.commit.assert_called_once()

    @patch('app.bizlogic.users.get_user_query')
    def test_get_user_returns_user(self, mock_get_query):
        """Test that get_user returns user data"""
        from app.bizlogic.users import get_user

        mock_conn = Mock()
        mock_get_query.return_value = {"id": 1, "name": "Alice"}

        result = get_user(mock_conn, 1)

        assert result["name"] == "Alice"
        mock_get_query.assert_called_once_with(mock_conn, user_id=1)

    @patch('app.bizlogic.users.list_users_query')
    def test_list_users_returns_list(self, mock_list_query):
        """Test that list_users returns list of users"""
        from app.bizlogic.users import list_users

        mock_conn = Mock()
        mock_list_query.return_value = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]

        result = list_users(mock_conn)

        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        mock_list_query.assert_called_once_with(mock_conn)