from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("thisismypassword")
password2 = sha256_crypt.encrypt("thisismypassword")

p = ("thisismypassword")
p1 = ("thisismypassword")

print(password)
print(password2)

print(sha256_crypt.verify(p, password))