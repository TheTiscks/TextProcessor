from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

def encrypt_aes_gcm(plaintext: bytes, key: bytes) -> str:
    aesgcm = AESGCM(key)
    iv = os.urandom(12)
    ct = aesgcm.encrypt(iv, plaintext, None)
    # хранить iv + ct в base64
    return base64.b64encode(iv + ct).decode()

def decrypt_aes_gcm(b64: str, key: bytes) -> bytes:
    raw = base64.b64decode(b64)
    iv, ct = raw[:12], raw[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(iv, ct, None)