"""WTForms: guestbook post (CSRF protected)."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class GuestbookForm(FlaskForm):
    """Username + content only."""

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=1, max=64)],
        render_kw={"placeholder": "Your name", "class": "input"},
    )
    content = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(max=2000)],
        render_kw={"placeholder": "Your message...", "rows": 4, "class": "input"},
    )
    submit = SubmitField("Post")
