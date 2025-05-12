import secrets

# 生成隨機的 SECRET_KEY（16字節）
secret_key = secrets.token_hex(16)
print(f"SECRET_KEY={secret_key}")

# 生成隨機的 JWT_SECRET_KEY（32字節）
jwt_secret_key = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY={jwt_secret_key}")

# 生成隨機的 API_KEY（32字節）
api_key = secrets.token_urlsafe(32)
print(f"API_KEY={api_key}")
