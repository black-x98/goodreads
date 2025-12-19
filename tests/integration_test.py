import requests

BASE_URL = "http://127.0.0.1:8000"

# ------------------------------
# Helper Functions
# ------------------------------
def post_json(endpoint, payload):
    resp = requests.post(f"{BASE_URL}{endpoint}", json=payload)
    try:
        data = resp.json()
    except Exception:
        data = resp.text
    print(f"POST {endpoint}:", resp.status_code, data)
    return resp, data

def get(endpoint):
    resp = requests.get(f"{BASE_URL}{endpoint}")
    try:
        data = resp.json()
    except Exception:
        data = resp.text
    print(f"GET {endpoint}:", resp.status_code, data)
    return resp, data

# ------------------------------
# Seed Data
# ------------------------------
print("\n--- Seeding Test Data ---")

# Create users
users_payload = [{"name": "Alice"}, {"name": "Bob"}]
user_ids = []
for u in users_payload:
    resp, data = post_json("/users", u)
    if resp.status_code == 200 and "id" in data:
        user_ids.append(data["id"])

# Create books
books_payload = [
    {"title": "Clean Code", "author": "Robert C. Martin"},
    {"title": "The Pragmatic Programmer", "author": "Andy Hunt"},
]
book_ids = []
for b in books_payload:
    resp, data = post_json("/books", b)
    if resp.status_code == 200 and "id" in data:
        book_ids.append(data["id"])

# ------------------------------
# Test Users Endpoints
# ------------------------------
print("\n--- Testing Users Endpoints ---")
get("/users")
for uid in user_ids:
    get(f"/users/{uid}")

# ------------------------------
# Test Books Endpoints
# ------------------------------
print("\n--- Testing Books Endpoints ---")
get("/books")
for bid in book_ids:
    get(f"/books/{bid}")

# ------------------------------
# Test Reviews Endpoints
# ------------------------------
print("\n--- Testing Reviews Endpoints ---")
# Add review for first book by first user
review_payload = {
    "user_id": user_ids[0],
    "book_id": book_ids[0],
    "rating": 5,
    "content": "Excellent book!"
}
post_json("/reviews", review_payload)

# List reviews by user
get(f"/users/{user_ids[0]}/reviews")
# List reviews by book
get(f"/books/{book_ids[0]}/reviews")

# ------------------------------
# Test Follow / Newsfeed Endpoints
# ------------------------------
print("\n--- Testing Follows / Newsfeed Endpoints ---")
# First user follows second user
post_json(f"/follow/{user_ids[1]}?follower_id={user_ids[0]}", {})

# Check newsfeed for first user
get(f"/users/{user_ids[0]}/newsfeed")

# First user unfollows second user
post_json(f"/unfollow/{user_ids[1]}?follower_id={user_ids[0]}", {})
