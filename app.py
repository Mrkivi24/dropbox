from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Database Models
class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_idea', methods=['POST'])
def submit_idea():
    content = request.form.get('idea')
    new_idea = Idea(content=content)
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        ideas = Idea.query.all()
        return render_template('dashboard.html', ideas=ideas)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
