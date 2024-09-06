import bcrypt

def encrypt_password(password: str) -> bytes:
    """
    加密密码
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password: bytes, user_password: str) -> bool:
    """
    验证密码
    """
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
