"""Separate Argon2id storage demo for one synthetic example only."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
_hasher=PasswordHasher()
def hash_password(synthetic_password): return _hasher.hash(synthetic_password)
def verify_password(synthetic_password,stored_hash):
    try: return _hasher.verify(stored_hash,synthetic_password)
    except VerifyMismatchError: return False
if __name__=="__main__":
    demo="Demo-Only-River-Quartz-2048!"; hashed=hash_password(demo)
    print("Synthetic demo hash:",hashed); print("Correct value verifies:",verify_password(demo,hashed))
