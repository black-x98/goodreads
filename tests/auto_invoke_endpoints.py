import requests

BASE_URL = "http://127.0.0.1:8000"

def safe_json(resp):
    try:
        return resp.json()
    except Exception:
        return resp.text or None

# ------------------------------
# Setup test data
# ------------------------------
def seed_data():
    print("--- Seeding Test Data ---")

    # Create users
    users = [
        {"name": "Alice"},
        {"name": "Bob"}
    ]
    created_users = []
    for u in users:
        resp = requests.post(f"{BASE_URL}/users", json=u)
        print("POST /users:", resp.status_code, safe_json(resp))
        if resp.status_code == 200 or resp.status_code == 201:
            created_users.append(safe_json(resp))

    # Create books
    books = [
        {"title": "Clean Code", "author": "Robert C. Martin"},
        {"title": "The Pragmatic Programmer", "author": "Andy Hunt"}
    ]
    created_books = []
    for b in books:
        resp = requests.post(f"{BASE_URL}/books", json=b)
        print("POST /books:", resp.status_code, safe_json(resp))
        if resp.status_code == 200 or resp.status_code == 201:
            created_books.append(safe_json(resp))

    return created_users, created_books


# ------------------------------
# Users Endpoints
# ------------------------------
def test_users():
    print("\n--- Testing Users Endpoints ---")
    resp = requests.get(f"{BASE_URL}/users")
    print("GET /users:", resp.status_code, safe_json(resp))

    resp = requests.get(f"{BASE_URL}/users/1")
    print("GET /users/1:", resp.status_code, safe_json(resp))


# ------------------------------
# Books Endpoints
# ------------------------------
def test_books():
    print("\n--- Testing Books Endpoints ---")
    resp = requests.get(f"{BASE_URL}/books")
    print("GET /books:", resp.status_code, safe_json(resp))

    resp = requests.get(f"{BASE_URL}/books/1")
    print("GET /books/1:", resp.status_code, safe_json(resp))


# ------------------------------
# Reviews Endpoints
# ------------------------------
def test_reviews():
    print("\n--- Testing Reviews Endpoints ---")
    review_data = {
        "user_id": 1,
        "book_id": 1,
        "rating": 5,
        "content": "Excellent book!"
    }

    # POST review
    resp = requests.post(f"{BASE_URL}/reviews", json=review_data)
    print("POST /reviews:", resp.status_code, safe_json(resp))

    # GET reviews by user
    resp = requests.get(f"{BASE_URL}/users/1/reviews")
    print("GET /users/1/reviews:", resp.status_code, safe_json(resp))

    # GET reviews by book
    resp = requests.get(f"{BASE_URL}/books/1/reviews")
    print("GET /books/1/reviews:", resp.status_code, safe_json(resp))


# ------------------------------
# Follow / Newsfeed Endpoints
# ------------------------------
def test_follows():
    print("\n--- Testing Follows / Newsfeed Endpoints ---")

    # Alice follows Bob (user 1 follows user 2)
    resp = requests.post(f"{BASE_URL}/follow/2", params={"follower_id": 1})
    print("POST /follow/2:", resp.status_code, safe_json(resp))

    # GET newsfeed for Alice (user 1)
    resp = requests.get(f"{BASE_URL}/users/1/newsfeed")
    print("GET /users/1/newsfeed:", resp.status_code, safe_json(resp))

    # Unfollow
    resp = requests.post(f"{BASE_URL}/unfollow/2", params={"follower_id": 1})
    print("POST /unfollow/2:", resp.status_code, safe_json(resp))


# ------------------------------
# Run All Tests
# ------------------------------
if __name__ == "__main__":
    seed_data()
    test_users()
    test_books()
    test_reviews()
    test_follows()
