# نمایش محصولات از دیتابیس روی لوکال

from flask import Flask, Response, render_template_string, send_file, request
import pyodbc
import pandas as pd
import io
import os
import sqlite3
from woocommerce import API
import time


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# تنظیمات اتصال به SQL Server لوکال
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=109.125.144.105\\WIN-F7CPTE3GRIV\\BACKUPSQL2014,1433;"          # یا localhost یا COMPUTERNAME\SQLEXPRESS
    "DATABASE=cy000402;"
    "UID=sa;"
    "PWD=123@abc;"
    "TrustServerCertificate=yes;"
)

# قالب HTML با جدول زیبا و فارسی درست
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>لیست کالاها - دیتابیس cy000402</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700&display=swap');
        body {font-family: 'Vazirmatn', Tahoma, sans-serif; background: #f8f9fa; margin: 0; padding: 20px; direction: rtl;}
        h1 {text-align: center; color: #2c3e50;}
        .container {max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);}
        table {width: 100%; border-collapse: collapse; margin-top: 20px;}
        th, td {padding: 12px 15px; text-align: right; border-bottom: 1px solid #ddd;}
        th {background: #007bff; color: white; font-weight: bold;}
        tr:nth-child(even) {background: #f8f9fa;}
        tr:hover {background: #e3f2fd;}
        .footer {margin-top: 30px; text-align: center; color: #666; font-size: 14px;}
        .search {width: 100%; padding: 12px; margin: 15px 0; font-size: 16px; border: 1px solid #ccc; border-radius: 8px;}
    </style>
</head>
<body>
    <div class="container">
    
        <div class="topbar">
            <a href="/backup" class="btn">📥 دانلود بکاپ اکسل</a>
        </div>
        <h1>لیست کالاها</h1>
        <p>دیتابیس: <strong>cy000402</strong> | تعداد کالا: <strong>{{ count }}</strong></p>
        
        <input type="text" id="search" class="search" placeholder="جستجو در نام یا کد کالا..." onkeyup="searchTable()">

        <table id="itemsTable">
            <thead>
                <tr>
                    <th>آیدی کالا</th>
                    <th>کد کالا</th>
                    <th>نام کالا</th>
                    <th>گروه کالا</th>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                <tr>
                    <td>{{ item.id }}</td>
                    <td>{{ item.code }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.group }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            بروزرسانی: {{ now }} | ساخته شده با Flask + Python
        </div>
    </div>

    <script>
        function searchTable() {
            let input = document.getElementById("search").value.toLowerCase();
            let rows = document.querySelectorAll("#itemsTable tbody tr");
            rows.forEach(row => {
                let text = row.textContent.toLowerCase();
                row.style.display = text.includes(input) ? "" : "none";
            });
        }
    </script>
</body>
</html>
"""
@app.route('/')
def index_page():
    try:
        # اتصال به فایل SQLite داخل پروژه
        conn = sqlite3.connect('data.db')
        conn.row_factory = sqlite3.Row  # این خط مهمه که دیکشنری بده
        cursor = conn.cursor()
        cursor.execute("SELECT ItemId, ItemCode, ItemDesc, ItemGroupDesc FROM items ORDER BY ItemId")
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append({
                "id": row["ItemId"] or "",
                "code": row["ItemCode"] or "",
                "name": row["ItemDesc"] or "بدون نام",
                "group": row["ItemGroupDesc"] or ""
            })

        from datetime import datetime
        now = datetime.now().strftime("%Y/%m/%d - %H:%M")

        return render_template_string(HTML_TEMPLATE, items=items, count=len(items), now=now)

    except Exception as e:
        import traceback
        return f"<pre>خطا:\n{traceback.format_exc()}</pre>", 500



server = "109.125.144.105\\WIN-F7CPTE3GRIV\\BACKUPSQL2014,1433"
database = "cy000402"
username = "sa"
password = "123@abc"
driver = "{ODBC Driver 17 for SQL Server}"  # مطمئن شوید روی سیستم شما نصب است

# تعریف connection_string قبل از اتصال
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"


if __name__ == '__main__':
    print("وب‌سرور در حال اجراست...")
    print("برای دیدن جدول، این آدرس را در مرورگر باز کن:")
    print("http://127.0.0.1:5000")
    print("برای خروج: Ctrl + C")
    app.run(host='127.0.0.1', port=5000, debug=False)
