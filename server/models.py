from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(
        db.String(10)
    )  # Assuming phone number is a 10-digit string
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    @validates("name")
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Author must have a name.")
        return name.strip()

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError("Phone number must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    @validates("title")
    def validate_title(self, key, title):
        if not title.strip():
            raise ValueError("Post must have a title.")
        return title.strip()

    @validates("content")
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary and len(summary) >= 250:
            raise ValueError("Summary must be less than or equal to 250 characters.")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if category not in valid_categories:
            raise ValueError(
                f'Invalid category. Valid categories are: {", ".join(valid_categories)}.'
            )
        return category

    @hybrid_property
    def is_clickbait(self):
        clickbait_words = ["amazing", "secret", "unbelievable"]
        return any(word in self.title.lower() for word in clickbait_words)

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})"