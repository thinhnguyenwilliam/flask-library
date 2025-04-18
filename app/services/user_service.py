from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def get_users():
    users = User.query.all()
    return users_schema.dump(users)

def create_user(data):
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"]  # In real apps, hash this!
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user)
