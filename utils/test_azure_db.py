# 測試雲端資料庫 Azure PostgreSQL Flexible Server 連線
import psycopg2
from backend.config import Config

if __name__ == "__main__":
    # 建立連線
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

    print("連線成功")

    # 關閉連線
    conn.close()
    print("連線已關閉")


