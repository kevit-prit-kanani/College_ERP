from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def get_hashed_password(password: str) -> str:
    return password_hash.hash(password)


def verify_hashed_password(plain_text: str, Hashed_pass: str):
    return password_hash.verify(password=plain_text, hash=Hashed_pass)
