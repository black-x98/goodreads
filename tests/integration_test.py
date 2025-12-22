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
# Fetch existing user and book IDs
# ------------------------------
print("\n--- Fetching Existing Data ---")

# Get all users
users_resp, users_data = get("/users")
user_ids = []
if isinstance(users_data, list) and len(users_data) > 0:
    # Extract unique user IDs, preferring seeded users (Alice, Bob, Charlie)
    seen_names = set()
    for user in users_data:
        if isinstance(user, dict) and 'name' in user and 'id' in user:
            # Only take first occurrence of each name to avoid duplicates
            if user['name'] not in seen_names:
                user_ids.append(user['id'])
                seen_names.add(user['name'])
    print(f"Found {len(user_ids)} unique users")
else:
    print("Warning: No users found in database")

# Get all books
books_resp, books_data = get("/books")
book_ids = []
if isinstance(books_data, list) and len(books_data) > 0:
    # Extract unique book IDs
    seen_titles = set()
    for book in books_data:
        if isinstance(book, dict) and 'title' in book and 'id' in book:
            # Only take first occurrence of each title to avoid duplicates
            if book['title'] not in seen_titles:
                book_ids.append(book['id'])
                seen_titles.add(book['title'])
    print(f"Found {len(book_ids)} unique books")
else:
    print("Warning: No books found in database")

# Check if we have enough data to run tests
if len(user_ids) < 2:
    print("ERROR: Need at least 2 users to run tests. Please seed the database first.")
    exit(1)

if len(book_ids) < 1:
    print("ERROR: Need at least 1 book to run tests. Please seed the database first.")
    exit(1)

# ------------------------------
# Test Users Endpoints
# ------------------------------
print("\n--- Testing Users Endpoints ---")
for uid in user_ids[:3]:  # Test first 3 users
    get(f"/users/{uid}")

# ------------------------------
# Test Books Endpoints
# ------------------------------
print("\n--- Testing Books Endpoints ---")
for bid in book_ids[:2]:  # Test first 2 books
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

print("\n--- Tests Complete ---")