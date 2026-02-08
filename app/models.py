"""Database models: guestbook posts only."""

from datetime import datetime

from app import db


class Post(db.Model):
    """Guestbook post: username + content."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post by {self.username!r}>"
