from Crypto.Cipher import AES


class PayloadEncryptor:
    def __init__(self, shared_key_hex: str):
        self.shared_key: bytes = shared_key_hex.encode()
        if len(self.shared_key) not in (16, 24, 32):
            raise ValueError("Invalid key length")

    def encrypt_payload(self, data: bytes) -> bytes:
        cipher = AES.new(self.shared_key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return nonce + ciphertext + tag

    def decrypt_payload(self, data: bytes) -> bytes:
        nonce = data[:16]
        ciphertext = data[16:-16]
        tag = data[-16:]
        cipher = AES.new(self.shared_key, AES.MODE_EAX, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data
