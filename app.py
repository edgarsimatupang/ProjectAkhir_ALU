from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)
    definition = db.Column(db.String(200), nullable=False)
    


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')
        words = Word.query.filter(or_(Word.word.ilike(f"%{search_query}%"), Word.definition.ilike(f"%{search_query}%"))).all()
    else:
        words = Word.query.all()
    
    return render_template('index.html', words=words)

@app.route('/add', methods=['POST'])
def add_word():
    try:
        word = request.form['word']
        definition = request.form['definition']
        
        new_word = Word(word=word, definition=definition)
        db.session.add(new_word)
        db.session.commit()

        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error adding word: {e}")
        return render_template('error.html', error_message="Failed to add word")
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        
