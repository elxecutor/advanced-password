import math
import re
import os

def load_common_passwords(filepath: str) -> set:
    """
    Load common passwords from a file into a set.
    Each password should be on a separate line.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return {line.strip().lower() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"Error: Could not find the file: {filepath}")
        return set()

# Build the file path relative to this script's directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
password_file = os.path.join(script_dir, "rockyou.txt")

COMMON_PASSWORDS = load_common_passwords(password_file)

# Common keyboard patterns to check (all in lowercase)
KEYBOARD_PATTERNS = ["qwerty", "asdfgh", "zxcvbn", "12345", "password", "admin"]

def calculate_base_entropy(password: str) -> float:
    pool = 0
    if re.search(r'[a-z]', password):
        pool += 26
    if re.search(r'[A-Z]', password):
        pool += 26
    if re.search(r'\d', password):
        pool += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        pool += 22
    return len(password) * math.log2(pool) if pool else 0.0

def penalty_for_repeated_and_sequential_patterns(password: str) -> float:
    penalty = 0.0
    # Repeated characters (3 or more in a row)
    if re.search(r'(.)\1{2,}', password):
        penalty += 10
    # Sequential patterns (e.g., 'abc', '123')
    for i in range(len(password) - 2):
        if ord(password[i+1]) - ord(password[i]) == 1 and ord(password[i+2]) - ord(password[i+1]) == 1:
            penalty += 5
        elif ord(password[i]) - ord(password[i+1]) == 1 and ord(password[i+1]) - ord(password[i+2]) == 1:
            penalty += 5
    # Keyboard patterns
    for pattern in KEYBOARD_PATTERNS:
        if pattern in password.lower():
            penalty += 10
    return penalty

def check_dictionary_words(password: str, dictionary: set) -> bool:
    lower_pwd = password.lower()
    if lower_pwd in dictionary:
        return True
    for i in range(len(lower_pwd)):
        for j in range(i + 4, len(lower_pwd) + 1):
            if lower_pwd[i:j] in dictionary:
                return True
    return False

def get_password_feedback(password: str, dictionary: set = None) -> (list, float):
    feedback = []
    penalty = penalty_for_repeated_and_sequential_patterns(password)
    
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("Password is too common.")
    if len(password) < 8:
        feedback.append("Password is too short; consider at least 8 characters.")
    if dictionary and check_dictionary_words(password, dictionary):
        feedback.append("Password contains dictionary words which makes it easier to guess.")
    if penalty > 0:
        feedback.append("Password contains repeated or sequential patterns which reduce its strength.")
    if len(password) < 12:
        feedback.append("Consider using a longer password for increased security.")
    if not re.search(r'[A-Z]', password):
        feedback.append("Adding uppercase letters can improve strength.")
    if not re.search(r'\d', password):
        feedback.append("Incorporating numbers can boost strength.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        feedback.append("Using special characters can further strengthen your password.")
    
    return feedback, penalty

def evaluate_password_strength(password: str, dictionary: set = None) -> dict:
    base_entropy = calculate_base_entropy(password)
    feedback, penalty = get_password_feedback(password, dictionary)
    effective_entropy = max(base_entropy - penalty, 0)
    
    if effective_entropy < 28:
        strength = "Very Weak"
    elif effective_entropy < 36:
        strength = "Weak"
    elif effective_entropy < 60:
        strength = "Moderate"
    elif effective_entropy < 128:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return {
        "password": password,
        "length": len(password),
        "base_entropy": base_entropy,
        "penalty": penalty,
        "effective_entropy": effective_entropy,
        "strength": strength,
        "feedback": feedback
    }
