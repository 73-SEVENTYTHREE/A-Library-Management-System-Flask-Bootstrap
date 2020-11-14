# encoding:utf-8
import os
from datetime import timedelta
SECRET_KEY='123456' #每次重启服务器的时候清除session
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI='mysql://root:2569535507Lw@127.0.0.1/library' #数据库配置 格式：mysql://账号:密码@127.0.0.1/COVID
PERMANENT_SESSION_LIFETIME=timedelta(days=1) #session有效期为1天
SQLALCHEMY_TRACK_MODIFICATIONS=False




