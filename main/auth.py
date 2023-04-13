from flask import Blueprint, redirect, url_for, request, render_template, flash, abort, make_response
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Users, db
from . import mail, login_manager


auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@auth.route("/login", methods=["POST", "GET"])
def login():

    # checking if method is post
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get("check")

        # making "Users" table query
        user_query = Users.query.filter_by(email=email).first()
        if user_query and check_password_hash(user_query.password, password):
            if remember == '1':
                login_user(user_query, remember=True)
            else:
                login_user(user_query)

            return redirect(url_for("views.index"))

        # if incorrect email or pass, flash them!
        else:
            flash("Incorrect login credentials!", category='error')
            return redirect(url_for("auth.login"))


    # determining where to redirect user
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))
    else:
        return render_template("/login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if not current_user.is_authenticated:

        if request.method == "POST":
            name = request.form.get('name')
            lname = request.form.get('lname')
            email = request.form.get('email')
            signup_pw = request.form.get('signup-password')
            confirm_pw = request.form.get('confirm-password')
            check = request.form.get('check')

            if check == '1':
                if not Users.query.filter_by(email=email).first():
                    if signup_pw == confirm_pw:
                        if len(signup_pw) > 5: 
                            create_user = Users(name=f"{name} {lname}", email=email, 
                                password=generate_password_hash(confirm_pw, method='sha256'))
                            db.session.add(create_user)
                            db.session.commit()
                            flash('Account created!', category='success')
                            return redirect(url_for('auth.login'))
                        else:
                            flash('Passwords must contain more than 5 characters!', category='error')
                            return redirect(url_for('auth.signup'))
                    else:
                        flash('Passwords does not match!', category='error')
                        return redirect(url_for('auth.signup'))
                else:
                    flash('This email already exists please consider signing in!', category='error')
                    return redirect(url_for('auth.signup'))


        return render_template('sign-up.html')
    else:
        return redirect(url_for('views.index'))


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('views.index'))
