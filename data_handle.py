"""
Data handling functions for blog application
"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
BLOGPOSTS = os.path.join(DATA_DIR, 'blogposts.json')


def load_blog_posts(filepath = BLOGPOSTS):
    """
    Load blog posts from JSON file.
    :param filepath: Path to the JSON file (defaults to BLOGPOSTS constant).
    :return: List of blog posts (list of dicts), or empty list if an error occurs.
    """
    try:
        with open(filepath, "r") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading blog posts from {filepath}: {e}")
        return []


def save_blog_posts(posts, filepath = BLOGPOSTS):
    """
    Save blog posts to JSON file.
    :param posts: List of blog posts to save (list of dicts).
    :param filepath: Path to the JSON file (defaults to BLOGPOSTS constant).
    :return: None
    """
    try:
        with open(filepath, "w") as handle:
            json.dump(posts, handle, indent=4)
    except (OSError, IOError) as e:
        raise RuntimeError(f"Failed to save blog posts to {filepath}: {e}") from e


def get_post_by_id(post_id):
    """
    Get a specific post by ID.
    :param post_id: ID of the blog post to retrieve.
    :return: Blog post as a dictionary, or None if not found.
    """
    posts = load_blog_posts()
    return next((post for post in posts if post["id"] == post_id), None)


def create_post(author, title, content):
    """
    Create a new blog post by generating a unique ID, construct the post data and save it to the json file.
    :param author: Author of the blog post.
    :param title: Title of the blog post.
    :param content: Content of the blog post.
    :return: None
    """
    posts = load_blog_posts()

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
    save_blog_posts(posts)


def update_post(post_id, data):
    """
    Update an existing blog post with given post ID.
    :param post_id: ID of the blog post to update.
    :param data: Dictionary containing updated fields of "author", "title" and "content".
    :return: None if post is not found
    """
    posts = load_blog_posts()
    post = next((post for post in posts if post["id"] == post_id), None)

    if post is None:
        return None

    # Update post fields
    post.update({
        "author": data["author"],
        "title": data["title"],
        "content": data["content"]
    })

    save_blog_posts(posts)


def delete_post(post_id):
    """
    Delete a blog post with given post ID.
    :param post_id: ID of the blog post to delete.
    :return: True if post was successfully deleted, False otherwise.
    """
    posts = load_blog_posts()
    initial_count = len(posts)

    posts = [post for post in posts if post["id"] != post_id]

    if len(posts) < initial_count:
        save_blog_posts(posts)
        return True
    return False


def like_post(post_id):
    """
    Increment likes for a post by 1.
    :param post_id: ID of the blog post to like.
    :return: Updated post as dictionary, or None if post not found.
    """
    posts = load_blog_posts()
    post = next((post for post in posts if post["id"] == post_id), None)

    if post is None:
        return None

    post["likes"] = post.get("likes", 0) + 1
    save_blog_posts(posts)
    return post