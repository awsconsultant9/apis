from jose import jwt

payload = {"user":123}

secret = "my_secret"

token = jwt.encode(payload, secret, algorithm="HS256")

print(token)

decoded = jwt.decode(token, secret, algorithms=["HS256", "RS256"])

print(payload.copy())
