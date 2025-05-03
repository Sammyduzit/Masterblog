"""
Data handling functions for blog application
"""
import json

# File path for blog data
BLOGPOSTS = "static/blogposts.json"


def load_json(filepath):
    """
    Load blog posts from JSON file.
    :param filepath: Path to the JSON file.
    :return: Parsed JSON data as a Python object, or empty list if an error occurs.
    """
    try:
        with open(filepath, "r") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(filepath, data):
    """
    Save blog posts to JSON file.
    :param filepath: Path to the JSON file.
    :param data: Data to be saved.
    :return: None
    """
    with open(filepath, "w") as handle:
        json.dump(data, handle, indent=4)


def get_all_posts():
    """
    Get all blog posts from json file.
    :return: List of blog posts (list of dicts), or empty list if no posts are found.
    """
    return load_json(BLOGPOSTS)


def save_all_posts(posts):
    """
    Save all blog posts to json file.
    :param posts: List of blog posts to save (list of dicts).
    :return: None
    """
    save_json(BLOGPOSTS, posts)


def get_post_by_id(post_id):
    """
    Get a specific post by ID.
    :param post_id: ID of the blog post to retrieve.
    :return: Blog post as a dictionary, or None if not found.
    """
    posts = get_all_posts()
    return next((post for post in posts if post["id"] == post_id), None)


def create_post(author, title, content):
    """
    Create a new blog post by generating a unique ID, construct the post data and save it to the json file.
    :param author: Author of the blog post.
    :param title: Title of the blog post.
    :param content: Content of the blog post.
    :return: None
    """
    posts = get_all_posts()

    # Generate new ID (handle empty list case)
    new_id = 1
    if posts:
        new_id = max(post["id"] for post in posts) + 1

    new_post = {
        "id": new_id,
        "author": author,
        "title": title,
        "content": content,
        "likes": 0
    }

    posts.append(new_post)
    save_all_posts(posts)


def update_post(post_id, data):
    """
    Update an existing blog post with given post ID.
    :param post_id: ID of the blog post to update.
    :param data: Dictionary containing updated fields of "author", "title" and "content".
    :return: None if post is not found
    """
    posts = get_all_posts()
    post = next((post for post in posts if post["id"] == post_id), None)

    if post is None:
        return None

    # Update post fields
    post.update({
        "author": data["author"],
        "title": data["title"],
        "content": data["content"]
    })

    save_all_posts(posts)


def delete_post(post_id):
    """
    Delete a blog post with given post ID.
    :param post_id: ID of the blog post to delete.
    :return: True if post was successfully deleted, False otherwise.
    """
    posts = get_all_posts()
    initial_count = len(posts)

    posts = [post for post in posts if post["id"] != post_id]

    if len(posts) < initial_count:
        save_all_posts(posts)
        return True
    return False


def like_post(post_id):
    """
    Increment likes for a post by 1.
    :param post_id: ID of the blog post to like.
    :return: Updated post as dictionary, or None if post not found.
    """
    posts = get_all_posts()
    post = next((post for post in posts if post["id"] == post_id), None)

    if post is None:
        return None

    post["likes"] = post.get("likes", 0) + 1
    save_all_posts(posts)
    return post


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


    errors = []

    # Check if all required fields are present
    required_fields = ["author", "title", "content"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        errors.append(f"Missing fields: {', '.join(missing_fields)}")

    # Validate each field
    for field in required_fields:
        if field in data:
            if not isinstance(data[field], str):
                errors.append(f"'{field}' must be a string.")
            elif not data[field].strip():
                errors.append(f"'{field}' cannot be empty.")

    # Return validation result
    return len(errors) == 0, errors