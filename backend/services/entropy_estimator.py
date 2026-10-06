"""Theoretical entropy upper-bound estimate; human choices are not uniform random."""
import math

def estimate_theoretical_entropy(password):
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() and not c.isspace() for c in password): pool += 33
    if any(c.isspace() for c in password): pool += 1
    return round(len(password) * math.log2(pool), 1) if password and pool else 0.0
