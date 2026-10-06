"""Local password analysis. Never persists, logs, or returns the password."""
from pathlib import Path
from .pattern_detector import detect_sequences, detect_keyboard_patterns, detect_repetition, detect_predictable_structure
from .entropy_estimator import estimate_theoretical_entropy
from .suggestion_engine import generate_suggestions

ROOT = Path(__file__).resolve().parents[2]
COMMON_FILE = ROOT / "data" / "common_passwords.txt"
def _common_words():
    try: return {x.strip().casefold() for x in COMMON_FILE.read_text(encoding="utf-8").splitlines() if x.strip() and not x.startswith("#")}
    except OSError: return {"password", "admin", "welcome", "letmein"}

def is_common_password(password):
    return password.casefold() in _common_words()

def analyze_length(password):
    n = len(password)
    band = "very short" if n < 8 else "short" if n < 12 else "better length" if n < 16 else "strong length contribution"
    return {"length": n, "band": band, "note": "Length contributes to strength but does not make predictable content secure."}

def analyze_password(password, context=None):
    if not isinstance(password, str): raise TypeError("Password must be text.")
    if len(password) > 1024: raise ValueError("Password exceeds the 1024-character analysis limit.")
    length = len(password)
    types = sum([any(c.islower() for c in password), any(c.isupper() for c in password), any(c.isdigit() for c in password), any(not c.isalnum() and not c.isspace() for c in password), any(c.isspace() for c in password)])
    unique = len(set(password))
    ratio = round(unique / length, 3) if length else 0.0
    common = is_common_password(password)
    sequences = detect_sequences(password)
    keyboard = detect_keyboard_patterns(password)
    repetition = detect_repetition(password)
    words = _common_words()
    structure = detect_predictable_structure(password, words - {password.casefold()})
    context_values = [str(v).casefold() for v in (context or {}).values() if isinstance(v, (str, int)) and len(str(v)) >= 3]
    personal = any(v in password.casefold() for v in context_values)
    findings = []
    def add(code, description, severity="medium"): findings.append({"code":code,"description":description,"severity":severity})
    if length < 12: add("short_length", "This password is short; longer passwords give more room for unpredictability.", "high")
    if common: add("common_password", "Your password matches a commonly used password pattern and should not be used.", "high")
    if types < 2 and length < 16: add("character_diversity", "The password uses a narrow character mix; consider a longer randomly generated option.")
    if sequences: add("sequence", "Predictable ascending or descending sequences were detected.")
    if keyboard: add("keyboard_pattern", "A familiar keyboard walk was detected.")
    if repetition: add("repetition", "Repeated characters or substrings reduce unpredictability.")
    if structure: add("predictable_structure", "A common word, trailing number, or year-like structure was detected.")
    if personal: add("personal_context", "The password appears to overlap with the optional context you supplied.", "high")
    if length >= 12 and ratio < 0.35: add("low_uniqueness", "Many characters repeat, reducing the value of the password's length.")
    length_points = min(35, length * 2.2)
    diversity_points = min(15, max(0, types - 1) * 4 + (3 if types >= 4 else 0))
    uniqueness_points = min(10, ratio * 10)
    pattern_points = 20 - min(20, 5*len(sequences) + 6*bool(keyboard) + 7*bool(repetition) + 5*bool(structure))
    common_points = 0 if common else 10
    unpredictability_points = min(10, max(0, (length-8) * .7 + ratio*4))
    penalty = (30 if common else 0) + (12 if keyboard else 0) + min(15, 5*len(sequences)) + (27 if repetition else 0) + (18 if personal else 0) + (27 if structure else 0)
    score = max(0, min(100, round(length_points+diversity_points+uniqueness_points+pattern_points+common_points+unpredictability_points-penalty)))
    if not password: score = 0
    label = "VERY WEAK" if score <= 20 else "WEAK" if score <= 40 else "MODERATE" if score <= 60 else "STRONG" if score <= 80 else "VERY STRONG"
    entropy = estimate_theoretical_entropy(password)
    findings.append({"code":"entropy_caveat","description":"Theoretical entropy is optimistic: this estimate assumes uniformly random character choices.","severity":"info"})
    metrics = {**analyze_length(password), "uppercase":any(c.isupper() for c in password), "lowercase":any(c.islower() for c in password), "digits":any(c.isdigit() for c in password), "symbols":any(not c.isalnum() and not c.isspace() for c in password), "spaces":any(c.isspace() for c in password), "unique_character_count":unique, "character_type_count":types, "unique_character_ratio":ratio, "theoretical_entropy_bits":entropy, "common_password":common, "sequences":sequences, "keyboard_patterns":keyboard, "repetition_types":repetition, "structure_types":structure, "personal_context_overlap":personal}
    suggestions = generate_suggestions(findings, length, score)
    return {"score":score,"classification":label,"findings":findings,"suggestions":suggestions,"metrics":metrics,"policy":{"status":"PASS" if length >= 12 and not common and not personal else "FAIL","minimum_length":12,"common_password_check":True,"personal_info_check":context is not None}}
