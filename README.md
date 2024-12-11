# Password Checker

Password Checker is a web-based tool that allows users to check the strength of their passwords and generate secure passwords using various methods. It provides insights into password strength based on multiple criteria and ensures adherence to strong password standards.

---

## Features

### 1. Password Strength Checker

- Evaluates passwords based on:
  - Length (minimum 8 characters).
  - Mix of uppercase and lowercase letters.
  - Presence of numbers.
  - Inclusion of special characters (e.g., `@`, `#`, `!`).
  - Avoidance of common passwords and keyboard patterns.
  - Repetition of characters (e.g., `aaa`).
- Provides detailed feedback on how to improve weak passwords.

### 2. Password Generator

- Generates secure passwords with two modes:
  - **Random character-based passwords**.
  - **Word-based passwords**, using a list of predefined words for readability.
- Allows customization of password length and word usage.

### 3. Empirical Study

- Measures performance for:
  - Time taken to determine each password strength factor.
  - Average generation times for word-based and character-based passwords.
  - Percentage of strong passwords generated.

---

## Installation

### Prerequisites

- Python 3.8 or later
- Flask
- pip (Python package installer)

### Steps

1. Clone the repository:
   ```bash
   git clone git@github.com:gyamfi01/Password_Checker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Password_Checker
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python password_checker.py
   ```
5. Open the application in your browser:
   ```
   http://127.0.0.1:5000
   ```

---

## Files

### 1. `password_checker.py`

- Main script implementing the password strength checker, generator, and empirical study.

### 2. `dashboard.html`

- Frontend for the web-based interface.

### 3. `common_passwords.txt`

- List of commonly used passwords to avoid.

### 4. `word_list.txt`

- List of words used for generating word-based passwords.

---

## How to Use

### Password Strength Checker

1. Enter a password in the "Check Password Strength" section.
2. Click **Check Strength**.
3. View feedback on the password's strength and suggestions for improvement.

### Password Generator

1. Specify the desired length of the password.
2. Enable or disable word-based passwords.
3. Click **Generate Password**.
4. View the generated password in the display area.

### Empirical Study

To run the empirical study, execute the script in study mode:

```bash
python password_checker.py study
```

The study will:

- Measure and display the time taken for each password strength factor.
- Compare word-based and character-based password generation times.
- Log and analyze the strength of generated passwords.

---

## Example Output

### Password Strength Checker

```
Strength: Weak
Feedback:
- ❌ Too short! Password must be at least 8 characters long.
- ❌ Missing a mix of upper and lower case letters.
- ❌ No special characters. Spice it up with @, #, or $!
```

### Password Generator

```
Generated Password: SkyBamboo74)
```

### Empirical Study

```
=== Password Strength Factor Times ===
Length Check: 0.001 ms
Upper/Lower Case Mix: 0.082 ms
...

=== Password Generation Times ===
Word-based: 0.006 ms
Regular: 0.009 ms

=== Password Strength Results ===
Word-based: 5/5 passed as Strong
Regular: 4/5 passed as Strong
```

---

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request with your improvements.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Axios](https://axios-http.com/)

