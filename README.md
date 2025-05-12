# 妙管家－家庭看護人力仲介平台後端伺服器程式

🏠 **我們的使命**  
妙管家致力於連結有需求的家庭與專業的看護人員，提供安心、便利的媒合服務，讓每一位家人都能獲得最合適的照顧。

## 🚀 專案簡介
本專案為「妙管家」後端伺服器，負責處理用戶帳號、訂單媒合、看護人力資料庫查詢等後端資料庫操作功能。

> 💡 **重要：**
>
> **本專案只含有API，沒有網頁伺服器功能。**
> 網頁伺服器是使用Expo建立ReactNative的Web server，以及可以透過安卓及ios上的Expo Go App透過網路下載與執行手機端client程式，另外可以透過esbuild打包成APK。

## 🛠️ 使用技術

- Python 3.13.2
- Flask Web Framework
- PostgreSQL 資料庫
- Azure App Service（伺服器端部署）
- Azure PostgreSQL Flexible Server（資料庫部署）

## ⚙️ 本地資料庫與雲端資料庫切換

此專案使用 `.env` 檔案來管理資料庫連線設定。  
如需切換資料庫來源（本地 / Azure 雲端），請設定：

```env
USE_AZURE_DB=true
```
## 📦 套件安裝
python -m venv venv # 建立虛擬環境
source venv/bin/activate  # 切換到虛擬環境 (Windows 用 venv\Scripts\activate)
pip install -r requirements.txt # 按照我的套件表安裝所有套件到venv

## Procfile 的寫法
要寫Procfile才能佈署在雲端，位於 `.\backend\Procfile`。
- `web:`代表告訴 Azure 或 Heroku 這是一個 Web 應用，會使用該行啟動。
- `gunicorn`是 Python WSGI server，用來在生產(Production)環境跑 Flask 應用，不會執行`app.py`裡面的`if __name__ == '__main__':`。
- `--bind`是指伺服器要綁定在哪個 IP 和 port 上運作，0.0.0.0 意思是「接受所有來源來的連線」。如果設成 127.0.0.1，就只有自己機器可以連，不會對外開放。
- `--timeout`是指設定「每個請求最多能執行幾秒」，超過就中斷。通常30～60 秒。
- `app:app`第一個`app`是`app.py`檔名（不含副檔名），第二個`app`是 Flask 物件名稱，要跟`app.py`裡面的`app = Flask(__name__)`變數名稱一樣。
```Procfile
web: gunicorn --bind=0.0.0.0 --timeout 30 app:app
```