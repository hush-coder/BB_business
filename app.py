from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Product, Message
from config import Config
from extensions import db
from datetime import datetime
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        invite_code = request.form.get('invite_code')

        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册')
            return redirect(url_for('register'))

        if role == 'admin' and invite_code != app.config['ADMIN_INVITE_CODE']:
            flash('管理员邀请码错误')
            return redirect(url_for('register'))

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        if role == 'factory':
            user.factory_name = request.form.get('factory_name')
            user.factory_description = request.form.get('factory_description')
        elif role == 'dealer':
            user.company_name = request.form.get('company_name')
            user.company_address = request.form.get('company_address')

        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出登录')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        users = User.query.all()
        products = Product.query.all()
        return render_template('admin_dashboard.html', users=users, products=products)
    elif current_user.role == 'factory':
        products = current_user.products.all()
        messages = current_user.received_messages.all()
        return render_template('factory_dashboard.html', products=products, messages=messages)
    else:  # dealer
        products = Product.query.filter_by(is_active=True).all()
        messages = current_user.received_messages.all()
        return render_template('dealer_dashboard.html', products=products, messages=messages)

@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'factory':
        flash('只有工厂可以添加产品')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            factory_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('产品添加成功')
        return redirect(url_for('dashboard'))

    return render_template('add_product.html')

@app.route('/message/send/<int:receiver_id>', methods=['POST'])
@login_required
def send_message(receiver_id):
    try:
        content = request.form.get('content')
        if not content:
            flash('消息内容不能为空', 'error')
            return redirect(url_for('dashboard'))

        receiver = User.query.get_or_404(receiver_id)
        message = Message(
            content=content,
            sender_id=current_user.id,
            receiver_id=receiver_id,
            created_at=datetime.utcnow()
        )
        db.session.add(message)
        db.session.commit()
        flash('消息发送成功', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'error')
        return redirect(url_for('dashboard'))

@app.route('/admin/approve_dealer/<int:dealer_id>')
@login_required
def approve_dealer(dealer_id):
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('dashboard'))

    dealer = User.query.get_or_404(dealer_id)
    if dealer.role == 'dealer':
        dealer.payment_status = True
        db.session.commit()
        flash('经销商已批准')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 