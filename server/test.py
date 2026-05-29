from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# 1. Генерация закрытого (private) и открытого (public) ключей
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

# 2. Шифрование сообщения открытым ключом
message = b"Top secret message"
print(type(public_key))
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# print("Зашифрованные данные (байт):", ciphertext)

# 3. Дешифрование сообщения закрытым ключом
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# print("Расшифрованное сообщение:", plaintext.decode('utf-8'))
