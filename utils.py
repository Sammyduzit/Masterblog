def validate_post_data(data):
    """
    Validates the structure and content of post data.
    Checks if the required fields "author", "title" and "content" exist and are valid (non-empty string)
    :param data: Dictionary containing blog post data.
    :return: tuple: (is_valid: bool, errors: list)
    """
    errors = []
    required_fields = {"author", "title", "content"}
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            continue

        if not isinstance(data[field], str):
            errors.append(f"'{field}' must be a string.")
        elif not data[field].strip():
            errors.append(f"'{field}' cannot be empty.")

    return len(errors) == 0, errors