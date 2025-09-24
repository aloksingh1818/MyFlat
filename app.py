from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///myflat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload directories
os.makedirs(os.path.join('static', 'uploads', 'images'), exist_ok=True)
os.makedirs(os.path.join('static', 'uploads', 'videos'), exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    flat_type = db.Column(db.String(20), nullable=False)  # 1RK, 2BHK, 3BHK, 4BHK, etc.
    location = db.Column(db.String(200), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    video_path = db.Column(db.String(200))
    contact_name = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(15), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    post_type = db.Column(db.String(20), default='flat')  # 'flat' or 'roommate'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('flats', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    flats = Flat.query.filter_by(is_available=True).order_by(Flat.created_at.desc()).all()
    return render_template('index.html', flats=flats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post_flat', methods=['GET', 'POST'])
@login_required
def post_flat():
    if request.method == 'POST':
        flat = Flat(
            title=request.form['title'],
            flat_type=request.form['flat_type'],
            location=request.form['location'],
            rent=int(request.form['rent']),
            description=request.form['description'],
            contact_name=request.form['contact_name'],
            contact_phone=request.form['contact_phone'],
            contact_email=request.form['contact_email'],
            post_type=request.form['post_type'],
            user_id=current_user.id
        )
        
        # Handle file uploads
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            if image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join('static', 'uploads', 'images', filename)
                image.save(image_path)
                flat.image_path = f'uploads/images/{filename}'
        
        if 'video' in request.files and request.files['video'].filename:
            video = request.files['video']
            if video.filename:
                filename = secure_filename(video.filename)
                video_path = os.path.join('static', 'uploads', 'videos', filename)
                video.save(video_path)
                flat.video_path = f'uploads/videos/{filename}'
        
        db.session.add(flat)
        db.session.commit()
        
        flash('Post created successfully!')
        return redirect(url_for('index'))
    
    return render_template('post_flat.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    flats = Flat.query.order_by(Flat.created_at.desc()).all()
    return render_template('admin.html', flats=flats)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    flat_type = request.args.get('type', '')
    post_type = request.args.get('post_type', '')
    
    flats_query = Flat.query.filter_by(is_available=True)
    
    if query:
        flats_query = flats_query.filter(
            db.or_(
                Flat.title.contains(query),
                Flat.location.contains(query),
                Flat.description.contains(query)
            )
        )
    
    if flat_type:
        flats_query = flats_query.filter_by(flat_type=flat_type)
    
    if post_type:
        flats_query = flats_query.filter_by(post_type=post_type)
    
    flats = flats_query.order_by(Flat.created_at.desc()).all()
    
    return render_template('search.html', flats=flats, query=query, flat_type=flat_type, post_type=post_type)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@myflat.com',
                phone='1234567890',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
    
    app.run(debug=True)