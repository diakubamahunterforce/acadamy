import requests

BASE_URL = "http://127.0.0.1:5000/api"

# 1. LOGIN
login_data = {
    "email": "test@gmail.com",
    "password": "linux"
}

login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)

print("LOGIN STATUS:", login_resp.status_code)
print("LOGIN RESPONSE:", login_resp.json())

token = login_resp.json().get("token")

if not token:
    print(" Falha no login")
    exit()

# 2. HEADERS com JWT
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# 3. TESTAR /my-courses
resp = requests.get(f"{BASE_URL}/my-courses", headers=headers)

print("\nMY COURSES STATUS:", resp.status_code)
print("RESPONSE:")
print(resp.json())