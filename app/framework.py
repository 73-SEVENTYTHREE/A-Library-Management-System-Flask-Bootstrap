from flask import render_template, url_for, flash, redirect,session,Blueprint
from app import db
from app.forms import LoginForm
from app.models import Admin


login = Blueprint('login', __name__)

@login.before_request
def before_login():
    if 'identity' in session:
        print(session['identity'])
        pass
    else:
        session['identity']='Unknown'
        pass


@login.route("/", methods=['GET', 'POST'])
def a():
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == Users.name and form.password.data == Users.pwd:
        admin = Admin.query.filter_by(ID=form.email.data, pwd=form.password.data).first()
        if admin:
            session['identity']='admin'
            session['ID']=admin.ID
            flash('登录成功!','success')
            return redirect(url_for('admin.index'))
        else:
            flash('登录失败！请检查账号和密码！','warning')
    return render_template('a.html', title='Login', form=form)

@login.route("/logout", methods=['GET', 'POST'])
def logout():
    # session.pop('name',None)
    # logout_user()
    session.clear()
    return redirect(url_for('.a'))