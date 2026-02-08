"""Database models for the blog application."""

from datetime import datetime

from flask_login import UserMixin

from app import bcrypt, db


class User(UserMixin, db.Model):
    """User model for authentication and post authorship."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship(
        "Post",
        backref="author",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    """Blog post model."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    author_display_name = db.Column(db.String(64), nullable=True)  # e.g. "Guest" when user_id is null

    def author_name(self):
        """Display name: author username if logged-in user, else author_display_name (e.g. Guest)."""
        if self.author:
            return self.author.username
        return self.author_display_name or "Guest"

    def can_edit_delete(self, user):
        """True if user is the author or an admin."""
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_admin", False):
            return True
        return self.author and self.author.id == user.id

    def __repr__(self):
        return f"<Post {self.title!r}>"
