from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='Tigres@1983',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Tigres@1983@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_world():
    return "Hello Flask!"

@app.route('/new/')
def query_string(greeting="hello"):
    query_val = request.args.get('greeting',greeting)
    return '<h1> the greeting is : {0}</h1>'.format(query_val)

#Removing query strings
@app.route('/user')
@app.route('/user/<name>')
def no_query_string(name='mina'):
    return '<h1> Hello there ! {}</h1>'.format(name)

#Example of how to render html using render_template from Flask
#When using render_template flask automatically search for the
#html file under the template folder.
@app.route('/temp')
def using_templates():
    return render_template('Hello.html')


@app.route('/watch')
def movies_2017():
    movie_list = ['movie 1'
                , 'movie 2'
                , 'movie 3'
                , 'movie 4'
                , 'movie 5']

    return render_template('movies.html',
                    movies=movie_list,
                    name='Harry')

@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe':02.14,
                  'neon demon':3.20,
                  'ghost in a shell':1.5,
                  'kong':3.5,
                  'john wick 2':02.52,
                  'spiderman: homecoming':1.48}

    return render_template('table_data.html',
                    movies=movies_dict,
                    name='Sally')

@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe':02.14,
                  'neon demon':3.20,
                  'ghost in a shell':1.5,
                  'kong':3.5,
                  'john wick 2':02.52,
                  'spiderman: homecoming':1.48}

    return render_template('filter_data.html',
                    movies=movies_dict,
                    name=None,
                    film='a christmas carol')

# class Publication(db.Model):
#     __tablename__ = 'publication'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#
#     def __init__(self,id,name):
#         self.id = id
#         self.name = name
#
#     def __repr__ (self):
#         return "The id is {}, Name is {}".format(self.id, self.name)

#By removing the id from __init__ it makes is an autonumeric when inserting
#to database.
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self,name):
        self.name = name

    def __repr__ (self):
        return "Publisher is {}".format(self.name)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    #Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__ (self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
