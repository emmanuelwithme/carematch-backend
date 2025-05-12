from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
import bcrypt

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# 用戶模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'caregiver' 或 'client'

with app.app_context():
    db.create_all()

@app.route('/api')
def index():
    return jsonify({'message': 'Hello, World!'}), 200

# 註冊
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 確保請求中包含必要的字段
    required_fields = ['email', 'password', 'name', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # 使用 bcrypt 加密密碼
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(
        email=data['email'],
        password=hashed_password.decode('utf-8'),  # 將 bytes 轉換為 str
        name=data['name'],
        role=data['role']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# 登入
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 確保請求中包含必要的字段
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

# 測試路由
@app.route('/api/test', methods=['GET'])
@jwt_required()
def test():
    current_user_id = get_jwt_identity()
    return jsonify({'message': 'Test successful', 'user_id': current_user_id})

@app.route('/api/users', methods=['GET'])
def get_all_users():
    client_key = request.headers.get('X-Api-Key')  # 自訂 header 名稱

    if client_key != app.config['API_KEY']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = User.query.all()
    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
        for user in users
    ]
    return jsonify(users_data), 200

# GET APK download URL
@app.route('/api/download')
def get_apk_download_url():
    return jsonify({
        # 這個要把APK上傳到microsoft azure blob storage
        'url': app.config['APK_DOWNLOAD_URL']
    }), 200

if __name__ == '__main__':
    # 使用 0.0.0.0 允許從任何 IP 地址訪問
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
