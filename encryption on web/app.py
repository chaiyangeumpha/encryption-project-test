from flask import Flask, render_template, request, send_file
from Crypto.Cipher import AES
import os
from decouple import config

app = Flask(__name__)

# 🔑 Key & IV (ดึงค่ามาจาก .env)
SECRET_KEY = config('SECRET_KEY').encode('utf-8')
IV = config('IV').encode('utf-8')


# ✅ ฟังก์ชันเข้ารหัสไฟล์
def encrypt_file(input_file_path, output_file_path):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

    with open(input_file_path, "rb") as f:
        file_data = f.read()

    # 🔹 Padding ให้ครบ 16-byte
    padding = 16 - (len(file_data) % 16)
    file_data += bytes([padding]) * padding

    encrypted_data = cipher.encrypt(file_data)

    with open(output_file_path, "wb") as f:
        f.write(encrypted_data)

    # 🗑 ลบไฟล์ต้นฉบับหลังจากเข้ารหัสเสร็จ
    os.remove(input_file_path)

# ✅ ฟังก์ชันถอดรหัสไฟล์
def decrypt_file(input_file_path, output_file_path):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

    with open(input_file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    # 🔹 ลบ Padding ออก
    padding = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding]

    with open(output_file_path, "wb") as f:
        f.write(decrypted_data)

    # 🗑 ลบไฟล์ต้นฉบับหลังจากถอดรหัสเสร็จ
    os.remove(input_file_path)

# 📌 Route แสดงหน้าเว็บ
@app.route("/")
def index():
    return render_template("index.html")

# 📌 Route สำหรับอัปโหลดและเข้ารหัสไฟล์
@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "file" not in request.files:
        return "ไม่มีไฟล์อัปโหลด", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "กรุณาเลือกไฟล์", 400

    # 📁 บันทึกไฟล์ต้นฉบับลง Temp
    input_path = os.path.join("uploads", file.filename)
    file.save(input_path)

    # 🔐 กำหนดชื่อไฟล์ที่เข้ารหัส
    encrypted_filename = file.filename + ".bin"
    encrypted_path = os.path.join("uploads", encrypted_filename)

    # 🔥 ทำการเข้ารหัสไฟล์
    encrypt_file(input_path, encrypted_path)

    # 📁 ส่งไฟล์ที่เข้ารหัสกลับให้ดาวน์โหลด
    return send_file(encrypted_path, as_attachment=True)

# 📌 Route สำหรับอัปโหลดและถอดรหัสไฟล์
@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "file" not in request.files:
        return "ไม่มีไฟล์อัปโหลด", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "กรุณาเลือกไฟล์", 400

    # 📁 บันทึกไฟล์ที่เข้ารหัสลง Temp
    input_path = os.path.join("uploads", file.filename)
    file.save(input_path)

    # 🔓 ตั้งชื่อไฟล์หลังถอดรหัส
    decrypted_filename = file.filename.replace(".bin", "")
    decrypted_path = os.path.join("uploads", decrypted_filename)

    # 🔥 ทำการถอดรหัสไฟล์
    decrypt_file(input_path, decrypted_path)

    # 📁 ส่งไฟล์ที่ถอดรหัสกลับให้ดาวน์โหลด
    return send_file(decrypted_path, as_attachment=True)

# 📌 Run Flask App
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)  # สร้างโฟลเดอร์เก็บไฟล์
    app.run(debug=True)