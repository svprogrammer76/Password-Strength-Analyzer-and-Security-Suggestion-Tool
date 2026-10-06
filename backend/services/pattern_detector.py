"""Local, educational password-pattern detectors."""
import re

SEQUENCES = tuple("0123456789"[i:i+4] for i in range(7)) + tuple("9876543210"[i:i+4] for i in range(7)) + tuple("abcdefghijklmnopqrstuvwxyz"[i:i+4] for i in range(23)) + tuple("zyxwvutsrqponmlkjihgfedcba"[i:i+4] for i in range(23))
KEYBOARD = ("qwerty", "asdf", "zxcv", "yuiop", "hjkl", "bnm", "qaz", "wsx", "edc", "rfv", "tgb", "yhn", "ujm")

def detect_sequences(password):
    value = password.casefold()
    return sorted({p for p in SEQUENCES if p in value}, key=lambda x: (len(x), x))

def detect_keyboard_patterns(password):
    value = password.casefold()
    return sorted({p for p in KEYBOARD if p in value})

def detect_repetition(password):
    findings = []
    if re.search(r"(.)\1{2,}", password, re.DOTALL):
        findings.append("repeated_characters")
    if re.search(r"(.{2,6})\1{1,}", password, re.DOTALL):
        findings.append("repeated_substring")
    return findings

def detect_predictable_structure(password, common_words=()):
    value = password.casefold()
    found = []
    if re.search(r"(?:19|20)\d{2}", value):
        found.append("year_pattern")
    if re.search(r"\d{2,}$", value):
        found.append("trailing_numbers")
    if any(w and w in value for w in common_words):
        found.append("common_word")
    return sorted(set(found))
