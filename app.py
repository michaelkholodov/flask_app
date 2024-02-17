from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from flask_restx import Api, Resource

ma = Marshmallow()
db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_db.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'
app.config['SECRET_KEY'] = 'asdfghjk'

admin = Admin(app, name='flask_app', template_mode='bootstrap4')

db.init_app(app)
ma.init_app(app)

api = Api(app, version='1.0', title='API', description='API Description')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)

class UserSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = User

class PostSerializer(ma.SQLAlchemySchema):
    class Meta:
        model = Post

@app.route('/')
def hello_world():
    return render_template('hello_world.html')

@api.route('/user_list/')
class UserList(Resource):
    def get(self):
        list_schema = UserSerializer(many=True)
        return list_schema.dump(User.query.all())

@api.route('/post_list/')
class PostList(Resource):
    def get(self):
        posts = Post.query.all()
        return render_template('post_list.html', posts=posts)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)