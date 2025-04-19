from app.extensions import db
from datetime import datetime, timezone

class Borrow(db.Model):
    __tablename__ = 'borrows'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    borrow_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    return_date = db.Column(db.DateTime(timezone=True), nullable=True)