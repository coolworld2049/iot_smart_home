from Crypto.Cipher import AES

from iot_smart_home.settings import settings


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


# Example usage
if __name__ == "__main__":
    encryptor = PayloadEncryptor(settings.shared_aes_key)

    plaintext = b"secret message"
    encrypted_data = encryptor.encrypt_payload(plaintext)
    decrypted_data = encryptor.decrypt_payload(encrypted_data)

    print("Original data:", plaintext)
    print("Encrypted data:", encrypted_data)
    print("Decrypted data:", decrypted_data)
