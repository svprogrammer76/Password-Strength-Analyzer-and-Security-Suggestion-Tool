"""Cryptographically secure demo password generation."""
import secrets
import string

def generate_password(length=20, uppercase=True, lowercase=True, numbers=True, symbols=True):
    if length not in (16, 20, 24): raise ValueError("Length must be 16, 20, or 24.")
    pools = []
    if uppercase: pools.append(string.ascii_uppercase)
    if lowercase: pools.append(string.ascii_lowercase)
    if numbers: pools.append(string.digits)
    if symbols: pools.append("!@#$%^&*()-_=+[]{}?")
    if not pools: raise ValueError("Choose at least one character group.")
    chars = [secrets.choice(pool) for pool in pools]
    alphabet = "".join(pools)
    chars.extend(secrets.choice(alphabet) for _ in range(length-len(chars)))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)
