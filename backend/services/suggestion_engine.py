"""Specific user-facing guidance, never echoing input text."""
def generate_suggestions(findings, length, score):
    suggestions = []
    codes = {f.get("code") for f in findings}
    if length < 16: suggestions.append("Consider a longer password or a passphrase made from randomly selected words.")
    if "common_password" in codes: suggestions.append("Your password matches a commonly used password pattern and should not be used.")
    if "sequence" in codes: suggestions.append("Remove predictable ascending or descending character sequences.")
    if "keyboard_pattern" in codes: suggestions.append("Avoid familiar keyboard walks such as qwerty.")
    if "repetition" in codes: suggestions.append("Replace repeated characters or repeated substrings with unpredictable content.")
    if "common_word" in codes or "predictable_structure" in codes: suggestions.append("Avoid common words with predictable numbers or years appended.")
    if "personal_context" in codes: suggestions.append("Avoid names, birth years, or organization details that others could know.")
    if "character_diversity" in codes and length < 16: suggestions.append("A password manager can create a longer, unique password without relying on a formula.")
    if score >= 60: suggestions.append("Use a different password for every account; a password manager helps prevent reuse.")
    suggestions.extend(["Enable multi-factor authentication (MFA) where available.", "Never reuse this password on another account."])
    return list(dict.fromkeys(suggestions))
