"""URL routes for the blog application."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms import LoginForm, PostForm, RegisterForm
from app.models import Post, User

bp = Blueprint("main", __name__)


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already in use.", "error")
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
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
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
@login_required
def post_new():
    """Create a new post (login required)."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("main.home"))
    return render_template("post_form.html", form=form, title="New post")


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    """Edit a post (author only)."""
    post = db.session.get(Post, post_id)
    if not post or post.author != current_user:
        flash("Post not found or you cannot edit it.", "error")
        return redirect(url_for("main.home"))
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("main.home"))
    return render_template("post_form.html", form=form, post=post, title="Edit post")


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    """Delete a post (author only)."""
    post = db.session.get(Post, post_id)
    if not post or post.author != current_user:
        flash("Post not found or you cannot delete it.", "error")
        return redirect(url_for("main.home"))
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("main.home"))
