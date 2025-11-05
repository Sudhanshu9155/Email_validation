def is_allowed_local_char(ch):
    return ch.isalnum() or ch in {'.', '_', '-', '+'}

def is_allowed_domain_char(ch):
    return ch.isalnum() or ch in {'-', '.'}

def validate_email(email: str) -> (bool, str):
    if email is None or email.strip() == "":
        return False, "Email cannot be empty."

    email = email.strip()

    if email.count('@') != 1:
        return False, "Email must contain exactly one '@'."

    local, domain = email.split('@', 1)

    if not local or not domain:
        return False, "Local or domain part missing."

    if local[0] == '.' or local[-1] == '.':
        return False, "Local part cannot start or end with a dot."
    if domain[0] == '.' or domain[-1] == '.':
        return False, "Domain cannot start or end with a dot."

    if '..' in local or '..' in domain:
        return False, "Consecutive dots not allowed."

    for ch in local:
        if not is_allowed_local_char(ch):
            return False, f"Invalid character '{ch}' in local part."

    if '.' not in domain:
        return False, "Domain must contain at least one dot."

    labels = domain.split('.')
    for label in labels:
        if not label:
            return False, "Invalid domain structure (empty label)."
        if label[0] == '-' or label[-1] == '-':
            return False, "Domain labels cannot start or end with '-'."
        for ch in label:
            if not is_allowed_domain_char(ch):
                return False, f"Invalid character '{ch}' in domain label."

    if len(labels[-1]) < 2:
        return False, "Top-level domain must have at least 2 letters."

    digit_count = sum(1 for ch in email if ch.isdigit())
    if digit_count < 3:
        return False, "Email must contain at least 3 number digits."

    return True, "✅ Email looks valid."


if __name__ == "__main__":
    email = input("Enter your email address: ")
    valid, message = validate_email(email)
    print(message)
