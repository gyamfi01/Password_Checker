from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re
import random
import time
from statistics import mean

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load common passwords and word list with error handling
def load_common_passwords(file_path="common_passwords.txt"):
    try:
        with open(file_path, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return set()

def load_word_list(file_path="word_list.txt"):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

common_passwords = load_common_passwords()
word_list = load_word_list()

# Global log to track generated passwords
password_log = []

# Password strength checker
# This function is one of the core components. It checks for key criteria like length, character diversity, and avoids predictable patterns.
def check_password_strength(password):
    feedback = []

    if len(password) < 8:
        feedback.append("❌ Too short! Password must be at least 8 characters long.")
    else:
        feedback.append("✅ Good length!")

    if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
        feedback.append("❌ Missing mix of upper and lower case letters.")
    else:
        feedback.append("✅ Nice mix of upper and lower case letters!")

    if not re.search("[0-9]", password):
        feedback.append("❌ Missing a number. Numbers make it stronger!")
    else:
        feedback.append("✅ Great! You've got numbers.")

    if not re.search(r"[!@#$%^&*()\-=_+]", password):
        feedback.append("❌ No special characters. Spice it up with @, #, or $!")
    else:
        feedback.append("✅ Special character is included.")

    if password.lower() in common_passwords:
        feedback.append("❌ Oh no! This is too common and easy to guess.")
    else:
        feedback.append("✅ Unique choice. Well done!")

    if re.search(r"(.)\1\1", password):
        feedback.append("❌ Avoid using repeated characters (e.g., 'aaa').")
    else:
        feedback.append("✅ No repeated characters.")

    keyboard_patterns = [
        "qwerty", "asdf", "zxcv", "1234", "5678", "7890", "abcd", "efgh", "ijkl",
        "mnop", "qrst", "uvwx", "yz", "0987", "8765", "4321"
    ]
    if any(pattern in password.lower() for pattern in keyboard_patterns):
        feedback.append("❌ Avoid predictable patterns like 'qwerty' or '1234'.")
    else:
        feedback.append("✅ No keyboard patterns detected.")

    strength = "Weak" if any("❌" in f for f in feedback) else "Strong"
    return strength, feedback

# Password generator with logging
# This function creates passwords and logs them for later analysis. It supports both word-based and fully randomized approaches.
def generate_password(length=12, use_words=False):
    global password_log  # Use the global log
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")
    
    if use_words:
        words = random.sample(word_list or ["defaultWord1", "defaultWord2"], 2)
        numbers = str(random.randint(10, 99))
        special_char = random.choice("!@#$%^&*()-_+=")
        password = "".join(words) + numbers + special_char

        if len(password) < length:
            extra_chars = random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 
                                         k=length - len(password))
            password += "".join(extra_chars)
        
        # Log the password
        strength, feedback = check_password_strength(password)
        password_log.append({
            "type": "Word-based",
            "password": password,
            "strength": strength,
            "feedback": feedback
        })
        return password

    lower = random.choice("abcdefghijklmnopqrstuvwxyz")
    upper = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    digit = random.choice("0123456789")
    special_char = random.choice("!@#$%^&*()-_+=")
    remaining = random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=", 
                                k=length - 4)
    password = [lower, upper, digit, special_char] + remaining
    random.shuffle(password)
    password = "".join(password)

    # Log the password
    strength, feedback = check_password_strength(password)
    password_log.append({
        "type": "Regular",
        "password": password,
        "strength": strength,
        "feedback": feedback
    })
    return password

# Display the password log
# I use this function to output all generated passwords and their feedback in a neat table format.
def display_combined_table():
    print("\n=== Password Log Table ===")
    print(f"{'Type':<12}{'Password':<20}{'Strength':<10}{'Feedback':<60}")
    print("=" * 100)
    for entry in password_log:
        feedback_str = "; ".join(entry["feedback"])
        print(f"{entry['type']:<12}{entry['password']:<20}{entry['strength']:<10}{feedback_str[:60]}...")
    print("=" * 100)

# Empirical study
# This function answers research questions about the tool's performance and reliability by testing password generation and checking.
def empirical_study():
    global password_log  # Use the global log
    password_log.clear()  # Clear previous logs before the study

    # Define counters and timers
    total_word_based_time = 0
    total_regular_time = 0
    word_based_passed = 0
    regular_passed = 0

    # Generate and evaluate 5 word-based and 5 regular passwords
    for _ in range(5):
        # Generate word-based password
        start_time = time.time()
        word_password = generate_password(length=12, use_words=True)
        total_word_based_time += (time.time() - start_time) * 1000  # Convert to ms
        word_strength, _ = check_password_strength(word_password)
        if word_strength == "Strong":
            word_based_passed += 1

        # Generate regular password
        start_time = time.time()
        regular_password = generate_password(length=12, use_words=False)
        total_regular_time += (time.time() - start_time) * 1000
        regular_strength, _ = check_password_strength(regular_password)
        if regular_strength == "Strong":
            regular_passed += 1

    # Calculate average generation times
    avg_word_based_time = total_word_based_time / 5
    avg_regular_time = total_regular_time / 5

    # Display password log
    display_combined_table()

    print("\n=== Password Generation Times (ms) ===")
    print(f"{'Type':<15}{'Average Time (ms)':<10}")
    print("=" * 50)
    print(f"Word-based       {avg_word_based_time:.3f}")
    print(f"Regular          {avg_regular_time:.3f}")
    print("=" * 50)

    print("\n=== Password Strength Results ===")
    print(f"Word-based: {word_based_passed}/5 passed as Strong")
    print(f"Regular: {regular_passed}/5 passed as Strong")
    print("=" * 50)


# Flask routes
# These routes handle the interactive parts of the app, letting users check passwords and generate new ones.
@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password")
    if not password:
        return jsonify({"error": "No password provided"}), 400
    strength, feedback = check_password_strength(password)
    return jsonify({"strength": strength, "feedback": feedback})

@app.route("/generate_password", methods=["POST"])
def generate_password_route():
    data = request.get_json()
    length = int(data.get("length", 12))
    use_words = data.get("use_words", False)
    password = generate_password(length, use_words)
    return jsonify({"password": password})

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "study":
        empirical_study()
    else:
        app.run(debug=True)
