from Crypto.Cipher import AES
import os
from decouple import config


# 🔑 Key & IV (ดึงค่ามาจาก .env)
SECRET_KEY = config('SECRET_KEY').encode('utf-8')
IV = config('IV').encode('utf-8')


# ✅ ฟังก์ชันเข้ารหัสไฟล์รูป (Encryption)
def encrypt_image(input_file, output_file):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

    with open(input_file, "rb") as f:
        file_data = f.read()

    # 🔹 Padding ให้ครบ 16-byte
    padding = 16 - (len(file_data) % 16)
    file_data += bytes([padding]) * padding

    encrypted_data = cipher.encrypt(file_data)

    with open(output_file, "wb") as f:
        f.write(encrypted_data)

    print(f"🔐 รูปภาพถูกเข้ารหัสแล้ว: {output_file}")

# 🔓 ฟังก์ชันถอดรหัสไฟล์รูป (Decryption)
def decrypt_image(input_file, output_file):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

    with open(input_file, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    # 🔹 ลบ Padding ที่เติมไว้
    padding = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding]

    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    print(f"🔓 รูปภาพถูกถอดรหัสแล้ว: {output_file}")

# 🔥 ทดสอบการเข้ารหัสและถอดรหัส
if __name__ == "__main__":
    input_file = "uploads/1KmBWtR8NxNAEJilkyTqqwVALNL4y6SlF=s2048.png"  # ไฟล์รูปภาพต้นฉบับ
    encrypted_file = "uploads/test_encrypted.bin"  # ไฟล์ที่ถูกเข้ารหัส
    decrypted_file = "uploads/test_decrypted.jpg"  # ไฟล์รูปที่ถอดรหัสกลับมา

    encrypt_image(input_file, encrypted_file)
    decrypt_image(encrypted_file, decrypted_file)