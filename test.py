from cryptography.fernet import Fernet   
key = Fernet.generate_key()
print(key)
f = Fernet(key)
token = f.encrypt(b"pass")
print(token)
print(f.decrypt(token))