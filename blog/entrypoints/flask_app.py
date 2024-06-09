from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.route("/add_blog_post", methods=["POST"])
def add_blog_post() -> str:
    print(request.json)
    return "OK"


@app.route("/blog_posts", methods=["GET"])
def get_blog_posts() -> str:
    return render_template_string("<p>Hello World!</p>")
