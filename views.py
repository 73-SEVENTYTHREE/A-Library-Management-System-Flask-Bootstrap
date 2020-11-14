from app.framework import login
from app import app
from app.admin import admin
from app.models import Admin,Book,Card,Borecord
from app import db
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(login, url_prefix='/')
#测试数据
db.drop_all()
db.create_all()
A1 = Admin(ID='admin', pwd='123456', email='2569535507@qq.com',name='张三')
db.session.add(A1)
db.session.commit()
B1=Book(number='100000',name='C++ primer',publisher='浙江大学出版社',type='自然科学',year='2002',author='张三',price='20.6',total=20,stock=0)
B2=Book(number='100001',name='Java入门',publisher='浙江大学出版社',type='自然科学',year='2010',author='李四',price='50.5',total=30,stock=1)
B3=Book(number='100002',name='哲学',publisher='浙江大学出版社',type='社会科学',year='2018',author='王五',price='41',total=15,stock=14)
db.session.add_all([B1,B2,B3])
db.session.commit()
card1=Card(number='zju3180100000',name='李四',department='计算机学院',type='学生')
db.session.add(card1)
db.session.commit()
record1=Borecord(book_number='100000',card_number='zju3180100000',borrow_date='2020-06-01',return_date='2020-06-10',dealer='admin')
db.session.add(record1)
db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
