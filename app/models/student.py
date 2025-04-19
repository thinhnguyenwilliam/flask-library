from app.extensions import db
from datetime import datetime, timezone

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    student_class = db.Column('class', db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    borrows = db.relationship('Borrow', backref='student', lazy=True)


    def __repr__(self):
        return f"<Student {self.name}>"

    def __str__(self):
        return f"{self.name} ({self.email})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'student_class': self.student_class,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
