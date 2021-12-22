from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nikita'}
    posts =[
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Poland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Василий'},
            'body': 'Привет!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

