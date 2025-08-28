import hashlib
import os

PASS_FILE = "password.txt"

# Parol fayli yo‘q bo‘lsa, standart parolni saqlaydi
def init_password():
    if not os.path.exists(PASS_FILE):
        with open(PASS_FILE, "w") as f:
            f.write(hashlib.sha256("admin123".encode()).hexdigest())

def get_password_hash():
    with open(PASS_FILE, "r") as f:
        return f.read().strip()

def check_password(input_password: str) -> bool:
    return hashlib.sha256(input_password.encode()).hexdigest() == get_password_hash()

def change_password(new_password: str):
    with open(PASS_FILE, "w") as f:
        f.write(hashlib.sha256(new_password.encode()).hexdigest())
