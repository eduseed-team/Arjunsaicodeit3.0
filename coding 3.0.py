from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'ME'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coding.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    details = db.relationship('Detail', backref='user', lazy=True)
class Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __init__(self, name, author, date, user_id):
        self.name = name
        self.author = author
        self.date = date
        self.user_id = user_id
@app.route('/login')
def login():
    return render_template('login 3.0.html')
@app.route('/switch', methods=['POST'])
def switch():
    username = request.form.get("First_name")
    if not username:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect(url_for('home'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/')
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    username = session.get('username')
    books = Detail.query.filter_by(user_id=user_id).all()
    return render_template('coding 3.0.html', books=books, name=username)
@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('activity')
        author = request.form.get('times')
        date = request.form.get('date')
        if name and author and date:
            new_entry = Detail(name, author, date, user_id)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add 3.0.html')
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        book_id = request.form.get('id')
        book = Detail.query.filter_by(id=book_id, user_id=user_id).first()
        if not book:
            return redirect(url_for('home'))
        book.name = request.form.get('activity')
        book.author = request.form.get('times')
        book.date = request.form.get('date')
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book = Detail.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return redirect(url_for('home'))
    return render_template('edit 3.0.html', books=book)
@app.route('/delete')
def delete():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    delete_id = request.args.get('id')
    book = Detail.query.filter_by(id=delete_id, user_id=user_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('home'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)