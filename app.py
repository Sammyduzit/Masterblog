from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import data_handle
import utils

app = Flask(__name__)


@app.route("/")
def index():
    """
    Display home page with all blog posts by retrieving all posts via the data handler
    and passing them to the index.html template.
    :return: Rendered html template for the home page.
    """
    blogposts = data_handle.load_blog_posts()
    return render_template("index.html", blogposts=blogposts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Adding a new blog post. If request is POST:
        - Validates submitted data (form or json).
        - Creates new blog post if data is valid, otherwise error message
        - Redirects to the home page after blog is created
    For GET request:
        - Renders add.html template for creating a new post.
    :return: Redirect to the home page if POST request blog is created,
                or rendered `add.html` template for GET request.
    """
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form.to_dict()

        #validate submitted data
        is_valid, errors = utils.validate_post_data(data)
        if not is_valid:
            return jsonify({"errors": errors}), 400

        data_handle.create_post(data["author"], data["title"], data["content"])
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """
    Delete a blog post by post ID. If post does not exist, returns 404 error.
    :param post_id: ID of the blog post to delete
    :return: Redirect to home page if successful, or 404 error if post not found.
    """
    success = data_handle.delete_post(post_id)
    if not success:
        abort(404, description="Post not found")
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """
    Update existing blog post by post ID.
    For POST request:
        - Validates submitted data (form or json).
        - Updates blog post if data is valid, otherwise error message.
        - Redirects to the home page after successful update.
    For GET request:
        - Renders update.html with the data of the blog post to be updated.
    :param post_id: ID of the blog post to update.
    :return: Redirect to the home page on success,
                rendered `update.html` template on GET,
                or 404 error if the post is not found.
    """
    post = data_handle.get_post_by_id(post_id)
    if post is None:
        abort(404, description="Post not found")

    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, errors = utils.validate_post_data(data)
        if not is_valid:
            return jsonify({"errors": errors}), 400

        data_handle.update_post(post_id, data)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>")
def like(post_id):
    """
    Increment the likes count for a blog post by 1.
    :param post_id: ID of the blog post to like.
    :return: Redirect to the home page on success,
                or 404 error if the post is not found.
    """
    post = data_handle.like_post(post_id)
    if post is None:
        abort(404, description="Post not found")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(e):
    """
    Handles 404 errors gracefully by rendering the error.html template to show the
    error message and a link to return to home.
    :param e: Error details.
    :return: Rendered html template for 404 error page.
    """
    return render_template("error.html", error=str(e)), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
