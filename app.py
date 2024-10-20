"""Blogly application."""

from flask import Flask, request, render_template, redirect 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db , User , Post
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "blogly_key"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

with app.app_context():
    db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Redirects to user list."""
    return redirect("/users")

@app.route("/users")
def list_page():
    """Shows list of users from the database."""
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new")
def add_page():
    """Show new user form."""
    return render_template("add_user.html") 

@app.route("/users/new", methods=['POST'])
def add_new():
    """Adds new user to the database."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def detail_user(user_id):
    """Show detail + posts of a user."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("details.html", user=user,posts=posts)

@app.route('/users/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def user_update_page(user_id):
    """Show the form to update a user."""
    user = User.query.get_or_404(user_id)
    return render_template("update.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update a user."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def add_post_page(user_id):
    """Show new post form."""
    user = User.query.get_or_404(user_id) 
    return render_template("add_post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_post(user_id):
    """Adds post to a page ."""
    user = User.query.get_or_404(user_id)
    title = request.form.get("title")
    content = request.form.get("content")

    new_post = Post(title=title, content=content, user_id=user.id)  

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/posts/<int:post_id>')
def detail_post(user_id,post_id):
    """Show Details of a POst ."""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template("detail_post.html", user=user,post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    """Delete a Post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def post_update_page(user_id,post_id):
    """Show the form to update a post."""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template("update_post.html", user=user,post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=['POST'])
def update_post(user_id, post_id):
    """Update a post."""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    post.title = request.form.get("title")
    post.content = request.form.get("content")
    
    db.session.commit()

    return redirect(f"/users/{user_id}")