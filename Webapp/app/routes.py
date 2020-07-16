from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User
import requests
from flask_session import Session
from flask import session


sess = Session()
sess.init_app(app)

@app.route('/')
@app.route('/index')
def index():
        return render_template('index.html')
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        print('User Found')
        return render_template('index.html', data=session['user'].name)
    form = LoginForm()
    jsonPayload = None
    if form.validate_on_submit():
        jsonPayload = {
                'username':form.username.data,
                'password':form.password.data
            }
        result = requests.post('http://0.0.0.0:5000/auth/login', json=jsonPayload)

        result = result.json()
        if result['status'] != 'fail':
            user = User(form.username.data,result['auth_token'],result['user']['user_id'])
            #print(user.uid)
            session['user'] = user
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('mydashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if 'user' in session:
        return redirect(url_for('mydashboard')) 
    form = RegistrationForm()
    jsonPayload = None
    if form.validate_on_submit():
        print('passed')
        jsonPayload = {
                'username':form.username.data,
                'email':form.email.data,
                'password':form.password.data,
                'phone':form.phone.data,
                'name':form.fname.data,
                'lname':form.lname.data,
                'gender':form.gender.data,
                'address':form.address.data,
                'city':form.city.data,
                'zipcode':form.zipcode.data,
                'state':form.state.data  
            } 
        print(jsonPayload)   
        result = requests.post('http://0.0.0.0:5000/auth/register', json=jsonPayload)

        result = result.json()
        if result['status'] == 'success':
            flash('Congratulations, you registered an account! Please verify your email first.')
            return redirect(url_for('login'))
        flash('The username or email have already registered.')
    return render_template('register.html', title='Register', form=form)


@app.route('/mydashboard', methods=['GET'])
def mydashboard():
    if 'user' in session:
        return render_template('mydashboard.html')
    else:
        return redirect(url_for('login'))
    
    
@app.route('/myaccount', methods=['GET'])
def myaccount():
    if 'user' in session:
        return render_template('myaccount.html')
    else:
        return redirect(url_for('login'))
    
