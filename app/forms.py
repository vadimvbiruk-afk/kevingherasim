"""WTForms for the blog application (includes CSRF protection via Flask-WTF)."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    """Registration form with CSRF token."""

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=64)],
        render_kw={"placeholder": "Username", "class": "input-field"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email", "class": "input-field"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Password", "class": "input-field"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm password", "class": "input-field"},
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Login form with CSRF token."""

    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email", "class": "input-field"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password", "class": "input-field"},
    )
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Log in")


class PostForm(FlaskForm):
    """Form for creating and editing blog posts (CSRF protected)."""

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)],
        render_kw={"placeholder": "Post title", "class": "input-field"},
    )
    content = TextAreaField(
        "Content",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Write your post...",
            "rows": 12,
            "class": "input-field w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-slate-500 focus:border-slate-500 resize-y min-h-[200px]",
        },
    )
    submit = SubmitField("Publish")
