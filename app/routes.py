"""Guestbook routes: home (list + create post)."""

from flask import Blueprint, flash, redirect, render_template, url_for

from app import db
from app.forms import GuestbookForm
from app.models import Post

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def home():
    """List posts (newest first) and handle new post (username + content)."""
    form = GuestbookForm()
    if form.validate_on_submit():
        post = Post(
            username=(form.username.data or "").strip() or "Anonymous",
            content=(form.content.data or "").strip(),
        )
        db.session.add(post)
        db.session.commit()
        flash("Message posted.", "success")
        return redirect(url_for("main.home"))
    posts = (
        db.session.execute(
            db.select(Post).order_by(Post.date_posted.desc())
        )
        .scalars()
        .all()
    )
    return render_template("home.html", form=form, posts=posts)
