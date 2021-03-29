import datetime

from flask import Flask, render_template, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.file import FileStorage
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from data.applications import Application
import os
from data import db_session
from data.news import News
from data.users import User
from data.train import Train
from forms import LoginForm, RegisterForm, TrainForm, DelTrain, ZayavkaForm, ProsmotrForm, AddNewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route('/index')
def index():
    return render_template("index.html", title='VegasDanceFamily')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/success')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Удачный вход')


@app.route('/cabinet')
@login_required
def cabinet():
    session = db_session.create_session()
    if current_user.sostav == 'N':
        return render_template('cabinet.html', name=current_user.name, surname=current_user.surname,
                               email=current_user.email, age=current_user.age, sostav='N')
    elif current_user.sostav == 'Y':
        tr = session.query(Train).filter(Train.sostav == current_user.sostav).all()
        train = []
        for i in tr:
            train.append([i.date, 'младший', i.dur])
        return render_template('cabinet.html', name=current_user.name, surname=current_user.surname,
                               email=current_user.email, age=current_user.age, sostav='Y', train=train)
    elif current_user.sostav == 'O':
        tr = session.query(Train).filter(Train.sostav == current_user.sostav).all()
        train = []
        for i in tr:
            train.append([i.date, 'старший', i.dur])
        return render_template('cabinet.html', name=current_user.name, surname=current_user.surname,
                               email=current_user.email, age=current_user.age, sostav='O', train=train)
    elif current_user.sostav == 'P':
        tr = session.query(Train).all()
        train = []
        for i in tr:
            train.append([i.date, 'старший' if i.sostav == 'O' else 'младший', i.dur])
        return render_template('cabinet.html', name=current_user.name, surname=current_user.surname,
                               email=current_user.email, age=current_user.age, sostav='P', train=train)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_train', methods=['GET', 'POST'])
@login_required
def add_train():
    if current_user.sostav != 'P':
        return redirect('/')
    else:
        form = TrainForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            fdate = datetime.datetime.combine(form.date.data.date(), form.time.data.time())
            if session.query(Train).filter(Train.date == fdate, Train.sostav == form.sostav.data).first():
                return render_template('add_train.html', form=form,
                                       message="У этого состава уже есть тренировка в это время")
            train = Train(
                date=fdate,
                sostav=form.sostav.data,
                dur=int(form.dur.data),
                user_id=int(current_user.id)
            )
            session.add(train)
            session.commit()
            return redirect('/success')
        return render_template('add_train.html', form=form)


@app.route('/delete_train', methods=['GET', 'POST'])
@login_required
def delete_train():
    if current_user.id != 1:
        return redirect('/')
    session = db_session.create_session()
    tr = session.query(Train).all()
    train = []
    for i in tr:
        train.append([i.date, 'старший' if i.sostav == 'O' else 'младший', i.dur])
    else:
        form = DelTrain()
        if form.validate_on_submit():
            session = db_session.create_session()
            trenirovka = session.query(Train).get(form.train_id.data)
            if not trenirovka:
                return render_template('delete_train.html', form=form, train=train,
                                       message="такой тренировки нету")

            session.delete(trenirovka)
            session.commit()
            return redirect('/success')
        return render_template('delete_train.html', form=form, train=train)


@app.route('/add_zayavka', methods=['GET', 'POST'])
@login_required
def add_zayavka():
    form = ZayavkaForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        applic = Application(
            sostav=form.sostav.data,
            about=form.about.data,
            user_id=int(current_user.id),
            podgotovka=form.podgotovka.data
        )
        session.add(applic)
        session.commit()
        return redirect('/success')
    return render_template('add_zayavka.html', form=form)


@app.route('/prosmotr_zayavok', methods=['GET', 'POST'])
@login_required
def prosmotr_zayavok():
    if current_user.sostav != 'P':
        return redirect('/')
    form = ProsmotrForm()
    session = db_session.create_session()
    if current_user.id == 1:
        zayavka = session.query(Application).first()
    else:
        zayavka = session.query(Application).filter(Application.sostav != "P").first()
    if form.validate_on_submit():
        if form.opin.data == 'True':
            session.delete(zayavka)
            user = zayavka.user
            user.sostav = zayavka.sostav
            session.merge(user)
            session.commit()
        else:
            session.delete(zayavka)
            session.commit()
        return redirect('/success')
    if zayavka:
        return render_template('prosmotr.html', form=form, zayavka=zayavka)
    else:
        return redirect('/empty')


@app.route('/news')
def news():
    session = db_session.create_session()
    new = session.query(News).all()
    new = list(reversed(new))
    return render_template('news.html', news=new)


@app.route('/newsadd', methods=['GET', 'POST'])
@login_required
def addnews():
    form = AddNewsForm()
    if current_user.sostav != 'P':
        return redirect('/')
    if form.validate_on_submit():
        new = News(
            title=form.title.data,
            content=form.content.data,
            upd_date=datetime.datetime.now()
        )
        if form.img.data:
            form.img.data.save('static/img/news/' + form.img.data.filename)
            new.img = 'static/img/news/' + form.img.data.filename
        session = db_session.create_session()
        session.add(new)
        session.commit()
        return redirect('/news')
    return render_template('addnews.html', form=form)


@app.route('/newsdel/<int:news_id>')
@login_required
def delnews(news_id):
    session = db_session.create_session()
    new = session.query(News).get(news_id)
    if new:
        if new.img:
            os.remove(new.img)
        session.delete(new)
        session.commit()
        return redirect('/news')
    else:
        abort(404)


@app.route('/newsput/<int:news_id>', methods=['GET', 'POST'])
@login_required
def putnews(news_id):
    form = AddNewsForm()
    session = db_session.create_session()
    new = session.query(News).get(news_id)
    if new:
        form.title.data = new.title
        form.content.data = new.content
        if new.img:
            form.img.data = FileStorage(stream=open(new.img), filename=new.img)
    else:
        abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        new = session.query(News).get(news_id)
        if new:
            new.title = form.title.data
            new.content = form.content.data
            if form.img.data:
                if form.img.data.filename != new.img:
                    os.remove(new.img)
                    form.img.data.save('static/img/news/' + form.img.data.filename)
                    new.img = 'static/img/news/' + form.img.data.filename
            session.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('addnews.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/blogs.sqlite')
    app.run(port=8080, host='127.0.0.1')
