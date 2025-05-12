import os
from dotenv import load_dotenv
import datetime

# 加載環境變量
load_dotenv()

class Config:
    # 選擇要用本地還是雲端資料庫
    USE_AZURE_DB: bool = os.getenv('USE_AZURE_DB').lower() == 'true'
    print(f"USE AZURE DB: {USE_AZURE_DB}")

    if USE_AZURE_DB:
        # Azure PostgreSQL Flexible Server 連線配置
        DB_TYPE = os.getenv('AZURE_DB_TYPE')
        DB_USER = os.getenv('AZURE_DB_USER')
        DB_PASSWORD = os.getenv('AZURE_DB_PASSWORD')
        DB_HOST = os.getenv('AZURE_DB_HOST')
        DB_PORT = os.getenv('AZURE_DB_PORT')
        DB_NAME = os.getenv('AZURE_DB_NAME')
    else:
        # 讀取資料庫相關配置
        DB_TYPE = os.getenv('DB_TYPE')
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')
        DB_NAME = os.getenv('DB_NAME')

    
    
    # 組合成完整的 DATABASE_URL
    SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)  # 15分鐘過期
    
    # 應用程序配置
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # 安全配置
    SECRET_KEY = os.getenv('SECRET_KEY')

    # 自己寫的API的KEY
    API_KEY = os.environ.get('API_KEY')

    # APK下載URL
    APK_DOWNLOAD_URL = os.environ.get('APK_DOWNLOAD_URL')
