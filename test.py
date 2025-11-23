import sqlite3
# دیگه نیازی به pyodbc نیست → کامل حذفش کن

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
