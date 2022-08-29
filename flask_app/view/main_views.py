import csv
import os
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_app import model_file
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import random
import pickle

model_file = os.path.join(os.getcwd(), 'flask_app', 'final_model.pkl')
db_connection_str = 'mysql+pymysql://root:Aktbzpf!95@127.0.0.1/myDB'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()
db = pymysql.connect(host= '127.0.0.1', user='root', password='Aktbzpf!95', db='myDB', charset='utf8') 

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods = ['GET'])
def index():
    return render_template('index.html')
@main_bp.route('/success',  methods=['POST'])
def success():
   if request.method == 'POST':
   	  # 변수 지정
      with open(model_file,'rb') as pickle_file:
        tmp = pickle.load(pickle_file)
      price = float(request.form['price']) 
      size = float(request.form['size'])
      weight = float(request.form['weight'])
      ram = float(request.form['ram'])
      cpu_score = float(request.form['cpu_score'])
      cpu_score = random.uniform(1090.25*(cpu_score-1), 1090.25*(cpu_score))
      gpu_score = float(request.form['gpu_score'])
      gpu_score = random.uniform(4296.375*(gpu_score-1), 4296.375*(gpu_score))
      passmark_score = float(request.form['passmark_score'])
      passmark_score = random.uniform(948.25*(passmark_score-1), 948.25*(passmark_score))
      try:
        ai_s = float(request.form['ai_s'])
      except:
        ai_s = 0
      try:
        ai_w = float(request.form['ai_w'])
      except:
        ai_w = 0
      try:
        ai_d = float(request.form['ai_d'])
      except:
        ai_d = 0
      try:
        ai_c = float(request.form['ai_c'])
      except:
        ai_c = 0
      try:
        ai_l = float(request.form['ai_l'])
      except:
        ai_l = 0
      try:
        ai_u = float(request.form['ai_u'])
      except:
        ai_u = 0
      try:
        ai_h = float(request.form['ai_h'])
      except:
        ai_h = 0
      X = [[price,size,weight,ai_s,ai_w,ai_d,ai_c,ai_l,ai_u,ai_h,ram,cpu_score,gpu_score,passmark_score]]
      SQL = f"SELECT 상품명 FROM label WHERE encoding = {tmp.predict(X)[0]}"
      y = pd.read_sql(SQL, db)
      url = f"https://search.shopping.naver.com/search/all?frm=NVSHMDL&pagingIndex=1&pagingSize=40&productSet=model&query={y.loc[0].values[0].replace(' ','%20')}&sort=rel&timestamp=&viewType=thumb"
      return render_template('success.html', model= y.loc[0].values[0],url = url) 
   else:
      pass