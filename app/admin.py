from flask import render_template, request, flash, make_response, url_for, redirect,Blueprint,session
from app import db
from app.models import Admin,Book,Borecord,Card
from io import BytesIO
from flask_mail import Mail, Message
from sqlalchemy import text
from app import mail
import datetime
admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET','POST'])
def index():
    return render_template('manager_index.html')

@admin.route('/manager_issue',methods=['GET','POST'])
def issue():
    if 'identity' in session and session['identity']=='admin': #如果身份是管理员就通过
        pass
    else:#否则返回用户界面
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('login.a'))
    if request.method == 'POST':
        number = request.form["number"]
        booktype = request.form["booktype"]
        bookname = request.form["bookname"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        author=request.form['author']
        price=request.form['price']
        quantity=request.form['quantity']
        q_number=Book.query.filter_by(number=number).first()
        if(q_number):
            current_num=q_number.stock
            current_total=q_number.total
            Book.query.filter_by(number=number).update({'total':current_total+number})
            Book.query.filter_by(number=number).update({'number': current_num + number})
            db.session.commit()
            flash("图书入库成功！",'success')
        else:
            try:
                new_book = Book(number=number,type=booktype,name=bookname,publisher=publisher,year=year,author=author,price=price,total=quantity,stock=quantity)
                db.session.add(new_book)
                db.session.commit()
                flash('图书入库成功！','success')
            except Exception as e:
                print(e)
                flash("入库出错！",'danger')
                db.session.rollback()
    return render_template("manager_issue.html")

@admin.route('/manager_query',methods=['GET','POST'])
def query():
    if request.method == 'POST':
        booktype = request.form["type"]
        print(booktype)
        bookname = request.form["name"]
        publisher = request.form["publisher"]
        start_year = request.form["start_year"]
        if(start_year==''):
            start_year=0
        end_year=request.form['end_year']
        if(end_year==''):
            end_year=99999
        author=request.form['author']
        min_price=request.form['min_price']
        max_price=request.form['max_price']
        if(min_price==''):
            min_price=0
        if(max_price==''):
            max_price=9999999
        results=Book.query.filter(
            Book.type.like('%'+booktype) if booktype is not None else text(""),
            Book.name.like('%' + bookname) if bookname is not None else text(""),
            Book.publisher.like('%' + publisher) if publisher is not None else text(""),
            Book.author.like('%' + author) if author is not None else text(""),
            Book.year >= start_year,
            Book.year <= end_year,
            Book.price >= min_price,
            Book.price <= max_price
        ).all()
        print(results)
        if(results):
            return render_template('results.html',results=results)
        else:
            flash('数据库内无相关书籍！','warning')
            return render_template('search.html')
    return render_template('search.html')

@admin.route('/manager_borrow',methods=['GET','POST'])
def borrow():
    if 'identity' in session and session['identity']=='admin': #如果身份是管理员就通过
        pass
    else:#否则返回用户界面
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('login.a'))
    borrowed_book=""
    if request.method=='POST':
        card_number=request.form['card_number']
        book_number=request.form['book_number']
        card=Card.query.filter_by(number=card_number).first()
        if(card is None):
            flash('数据库内无该借书证！','warning')
            return render_template('borrow.html',borrowed_book=borrowed_book)
        else:
            borrowed_book=card.borrowed_book
            print(borrowed_book)
            to_borrow=Book.query.filter_by(number=book_number).first()
            if(to_borrow is None):
                flash('数据库内无此书！','warning')
                return render_template('borrow.html', borrowed_book=borrowed_book)
            if(to_borrow.stock==0):
                latest_return=Borecord.query.filter_by(book_number=book_number).first()
                if(latest_return):
                    ldate=latest_return.return_date
                else:
                    ldate='空'
                flash('借书失败，库存不足！最近归还时间为：%s'%(ldate), 'warning')
                return render_template('borrow.html', borrowed_book=borrowed_book)
            else:
                time=datetime.date.today()
                admin_ID=session.get('ID')
                newstock=to_borrow.stock-1
                Book.query.filter_by(number=book_number).update({'stock':newstock})
                card.borrowed_book.append(to_borrow)
                db.session.commit()
                new_borrow_record=Borecord(book_number=book_number,card_number=card_number,borrow_date=time,dealer=admin_ID)
                db.session.add(new_borrow_record)
                db.session.commit()
                flash('借书成功！','success')
                borrowed_book=""
                return render_template('borrow.html',borrowed_book=borrowed_book)
    return render_template('borrow.html',borrowed_book=borrowed_book)

@admin.route('/manager_return',methods=['GET','POST'])
def book_return():
    if 'identity' in session and session['identity']=='admin': #如果身份是管理员就通过
        pass
    else:#否则返回用户界面
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('login.a'))
    borrowed_book=""
    if request.method=='POST':
        card_number=request.form['card_number']
        book_number=request.form['book_number']
        card=Card.query.filter_by(number=card_number).first()
        if(card is None):
            flash('数据库内无该借书证！','warning')
            return render_template('borrow.html',borrowed_book=borrowed_book)
        else:
            borrowed_book=card.borrowed_book
            print(borrowed_book)
            ifborrow =Borecord.query.filter_by(card_number=card_number,book_number=book_number,return_date=None).first()
            if(ifborrow):
                time=datetime.date.today()
                Borecord.query.filter_by(card_number=card_number,book_number=book_number,return_date=None).update({'return_date':time})
                the_book = Book.query.filter_by(number=book_number).first()
                newstock=the_book.stock+1
                Book.query.filter_by(number=book_number).update({'stock': newstock})
                print(borrowed_book)
                card.borrowed_book.remove(borrowed_book[0])
                db.session.commit()
                flash('还书成功！','success')
            else:
                flash('数据库内无该书被借记录！','warning')
    return render_template('return.html', borrowed_book=borrowed_book)

@admin.route('/manager_addcard',methods=['GET','POST'])
def addcard():
    if 'identity' in session and session['identity']=='admin': #如果身份是管理员就通过
        pass
    else:#否则返回用户界面
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('login.a'))
    if request.method=='POST':
        number=request.form['card_number']
        name=request.form['name']
        department=request.form['department']
        type=request.form['cardtype']
        q_card=Card.query.filter_by(number=number).first()
        if(q_card):
            flash('数据库内已存在该借书证！','warning')
            return render_template('card_manage.html')
        new_card=Card(number=number,name=name,department=department,type=type)
        db.session.add(new_card)
        db.session.commit()
        flash('添加借书证成功！','success')
    return render_template('card_manage.html')

@admin.route('/manager_deletecard',methods=['GET','POST'])
def deletecard():
    if 'identity' in session and session['identity']=='admin': #如果身份是管理员就通过
        pass
    else:#否则返回用户界面
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('login.a'))
    if request.method=='POST':
        number=request.form['card_number']
        q_card=Card.query.filter_by(number=number).first()
        if(q_card):
            borrowed_book=Borecord.query.filter_by(card_number=number,return_date=None).all()
            print(borrowed_book)
            if(borrowed_book):
                flash('该借书证还有未还书，无法注销！','warning')
                return render_template('card_manage.html')
            db.session.delete(q_card)
            db.session.commit()
            flash('删除借书证成功！','success')
        else:
            flash('数据库内无该借书证！','warning')
    return render_template('card_manage.html')

