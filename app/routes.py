"""URL routes for the blog application."""

import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms import LoginForm, PostForm, RegisterForm
from app.models import Post, User
from app.services.cloudinary_upload import upload_image

bp = Blueprint("main", __name__)


def admin_required(f):
    """Decorator: require authenticated admin."""
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            flash("Admin access required.", "error")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)

    return wrapped


@bp.route("/")
def home():
    """Home page route: list all posts newest first."""
    posts = (
        db.session.execute(
            db.select(Post).order_by(Post.date_posted.desc())
        )
        .scalars()
        .all()
    )
    return render_template("home.html", posts=posts)


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        admin_email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
        email_value = (form.email.data or "").strip().lower()
        user = User(
            username=(form.username.data or "").strip(),
            email=email_value or form.email.data,
            is_admin=bool(admin_email and email_value == admin_email),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already in use.", "error")
            return render_template("register.html", form=form)
        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Please try again.", "error")
            return render_template("register.html", form=form)
        flash("Registration successful. You can log in now.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in the user (form protected by CSRF via Flask-WTF)."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        email_value = (form.email.data or "").strip().lower()
        user = db.session.scalar(db.select(User).where(User.email == email_value))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))


@bp.route("/dashboard")
@login_required
def dashboard():
    """Dashboard visible only to authenticated users."""
    return render_template("dashboard.html")


@bp.route("/post/new", methods=["GET", "POST"])
def post_new():
    """Create a new post (logged-in user or guest)."""
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                author=current_user,
                author_display_name=None,
            )
        else:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                author=None,
                author_display_name="Guest",
            )
        image_file = request.files.get("image") or (form.image.data if hasattr(form.image, "data") else None)
        if image_file and image_file.filename:
            url = upload_image(image_file)
            if url:
                post.image_url = url
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("main.home"))
    return render_template("post_form.html", form=form, title="New post")


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def post_edit(post_id):
    """Edit a post (author or admin)."""
    post = db.session.get(Post, post_id)
    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("main.home"))
    if not post.can_edit_delete(current_user):
        flash("You do not have permission to edit this post.", "error")
        return redirect(url_for("main.home"))
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        image_file = request.files.get("image") or (form.image.data if hasattr(form.image, "data") else None)
        if image_file and image_file.filename:
            url = upload_image(image_file)
            if url:
                post.image_url = url
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("main.home"))
    return render_template("post_form.html", form=form, post=post, title="Edit post")


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
def post_delete(post_id):
    """Delete a post (author or admin)."""
    post = db.session.get(Post, post_id)
    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("main.home"))
    if not post.can_edit_delete(current_user):
        flash("You do not have permission to delete this post.", "error")
        return redirect(url_for("main.home"))
    if not current_user.is_authenticated:
        flash("You must be logged in to delete posts.", "error")
        return redirect(url_for("main.home"))
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("main.home"))


@bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    """Admin: list all posts with edit/delete."""
    posts = (
        db.session.execute(
            db.select(Post).order_by(Post.date_posted.desc())
        )
        .scalars()
        .all()
    )
    return render_template("admin/dashboard.html", posts=posts)


@bp.route("/admin/users")
@login_required
@admin_required
def admin_users():
    """Admin: list registered users (username, email)."""
    users = db.session.execute(db.select(User).order_by(User.created_at.desc())).scalars().all()
    return render_template("admin/users.html", users=users)
