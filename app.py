from flask import Flask, render_template, url_for, flash
from forms import RegistrationForm, LoginForm
from static.content import home_page, posts_page, error_page
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e65ad4591e69435f1016d9c587de2303'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    background_url = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"Post('{self.post_title}', '{self.date_posted}')"

# a = Post(post_title='Flask',
#          subtitle='The package that builds this website.',
#          date_posted=datetime.now(),
#          content='Some example texts.',
#          background_url='..\static\img\posts-banner.jpg')

# db.session.add(a)
# db.session.commit()
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html', content=error_page), 404

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('home.html', content=home_page)

@app.route('/posts', methods=['GET','POST'])
def posts_0():
    return render_template('posts.html', content=posts_page, posts=Post.query.all()[0:10])

@app.route('/posts/<page_num>', methods=['GET','POST'])
def posts(page_num):
    last_page_num = math.ceil(len(Post.query.all())/10)
    if page_num.isdigit() and last_page_num >= int(page_num):
        page_num = int(page_num)
        p = (page_num - 1) * 10
        q = page_num * 10
        if last_page_num > page_num:
            last_page = False
        else:
            last_page = True
        return render_template('posts.html', content=posts_page, posts=Post.query.all()[p:q],
                           page_num=page_num, last_page=last_page)
    else:
        return render_template('error404.html', content=error_page), 404


@app.route('/post/<post_id>', methods=['GET','POST'])
def post(post_id):
    if Post.query.get(post_id) != None:
        return render_template('post.html', content=Post.query.get(post_id))
    else:
        return render_template('error404.html'), 404

# @app.route('/register')
# def register():
#     form = RegistrationForm()
#     return render_template('register.html', form=form, title="zqtay's blog - Register")
#
# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', form=form, title="zqtay's blog - Login")


if __name__ == '__main__':
    #db.init_app(app)
    app.run(debug=True)

