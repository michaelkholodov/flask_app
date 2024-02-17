from app import ma
from app import User, Post


class UserSerializer(ma.SQLAlchemySchema):
    models = User

class PostSerializer(ma.SQLAlchemySchema):
    models = Post