import sqlite3
import os
from flask import Flask, request, escape

app = Flask(__name__)

# ❌ 1. SQL Injection 취약점
def get_user_info(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE id = {user_id}"  # 직접 문자열 삽입 → SQL Injection 위험
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    return result

# ❌ 2. XSS (Cross-Site Scripting)
@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    return f"Hello {name}!"  # 입력값을 필터링 없이 출력 → XSS 위험

# ❌ 3. 명령어 삽입 (Command Injection)
@app.route("/run")
def run():
    cmd = request.args.get("cmd", "ls")
    return os.popen(cmd).read()  # 입력값이 그대로 실행됨 → Command Injection 위험

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
