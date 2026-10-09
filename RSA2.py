from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def main():
    session_key_hex = input().strip()
    session_key_bytes = bytes.fromhex(session_key_hex)

    key = RSA.generate(1024)

    priv_key_pem = key.export_key()
    priv_key_text = priv_key_pem.decode('utf-8')

    pub_key_pem = key.publickey().export_key()
    pub_key_text = pub_key_pem.decode('utf-8')

    pub_key = RSA.import_key(pub_key_pem)
    cipher_rsa_encrypt = PKCS1_OAEP.new(pub_key)
    encrypted_bytes = cipher_rsa_encrypt.encrypt(session_key_bytes)

    priv_key = RSA.import_key(priv_key_pem)
    cipher_rsa_decrypt = PKCS1_OAEP.new(priv_key)
    decrypted_bytes = cipher_rsa_decrypt.decrypt(encrypted_bytes)

    print(priv_key_text)

    print(pub_key_text)

    print(encrypted_bytes.hex())

    print(decrypted_bytes.hex())

if __name__ == "__main__":
    main()