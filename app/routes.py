from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm, PostTweetForm
from app.email import send_reset_password_mail
from app.models import User, Post

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostTweetForm()
    if form.validate_on_submit():
        body = form.text.data
        post = Post(body=body)
        current_user.posts.append(post)
        db.session.commit()
        flash('Your have post new tweet', category='success')

    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registration success', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        # check password
        remember = form.remember.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Login success', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash("用戶不存在或密碼錯誤", category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
# @app.route('/login')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/send_password_reset_request', methods=["GET", "POST"])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash('Password reset request mail is sent, please check your email', category='info')
    return render_template('send_password_reset_request.html', form=form)


@app.route('/reset_password<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token=token)
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your reset is done, you can login now', category='info')
            return redirect(url_for('login'))
        else:
            flash('this user is not exist', category='info')
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
