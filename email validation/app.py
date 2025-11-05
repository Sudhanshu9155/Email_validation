from flask import Flask, render_template, request

app = Flask(__name__)

def is_allowed_local_char(ch):
    # letters, digits and a few symbols commonly allowed in local part
    return ch.isalnum() or ch in {'.', '_', '-', '+'}

def is_allowed_domain_char(ch):
    # letters, digits and hyphen and dot for domain labels
    return ch.isalnum() or ch in {'-', '.'}

def validate_email(email: str) -> (bool, str):
    """
    Return (is_valid, message).
    Implementation uses string ops and loops (no regex).
    Basic rules implemented:
      - exactly one '@'
      - local part non-empty, domain non-empty
      - no leading/trailing dots in local or domain
      - no consecutive dots in local or domain
      - local characters restricted to a conservative set
      - domain must contain at least one dot (.) and last label >= 2 chars
      - domain labels cannot start/end with '-'
      - must contain at least 3 digits in total
    """

    if email is None:
        return False, "No input."

    email = email.strip()
    if email == "":
        return False, "Email is empty."

    # 1. exactly one '@'
    if email.count('@') != 1:
        return False, "Email must contain exactly one '@'."

    local, domain = email.split('@', 1)

    # 2. Local and domain non-empty
    if local == "":
        return False, "Local part (before @) is empty."
    if domain == "":
        return False, "Domain part (after @) is empty."

    # 3. No leading/trailing dots
    if local[0] == '.' or local[-1] == '.':
        return False, "Local part must not start or end with a dot."
    if domain[0] == '.' or domain[-1] == '.':
        return False, "Domain must not start or end with a dot."

    # 4. No consecutive dots
    if '..' in local:
        return False, "Local part must not contain consecutive dots."
    if '..' in domain:
        return False, "Domain must not contain consecutive dots."

    # 5. Allowed characters in local
    for ch in local:
        if not is_allowed_local_char(ch):
            return False, f"Invalid character '{ch}' in local part."

    # 6. Domain checks
    if '.' not in domain:
        return False, "Domain must contain at least one dot (e.g., 'example.com')."

    labels = domain.split('.')
    for label in labels:
        if label == "":
            return False, "Domain has empty label (consecutive dots or leading/trailing dot)."
        if len(label) == 0:
            return False, "Empty domain label."
        if label[0] == '-' or label[-1] == '-':
            return False, "Domain labels must not start or end with '-' (hyphen)."
        for ch in label:
            if not (ch.isalnum() or ch == '-'):
                return False, f"Invalid character '{ch}' in domain label."

    if len(labels[-1]) < 2:
        return False, "Top-level domain (last label) must be at least 2 characters."

    if len(email) > 254:
        return False, "Email is too long (>254 characters)."

    # 7. Must contain at least 3 digits (0–9)
    digit_count = 0
    for ch in email:
        if ch.isdigit():
            digit_count += 1
    if digit_count < 3:
        return False, "Email must contain at least 3 digits."

    # Passed all checks
    return True, "Email looks valid (basic checks passed)."


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None, email='')

@app.route('/validate', methods=['POST'])
def validate():
    email = request.form.get('email', '')
    valid, message = validate_email(email)
    return render_template('index.html', result={'valid': valid, 'message': message}, email=email)

if __name__ == '__main__':
    app.run(debug=True)
