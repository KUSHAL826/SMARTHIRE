def validate_input(user_input):

    if not user_input or not user_input.strip():
        return False

    if len(user_input) > 2000:
        return False

    return True