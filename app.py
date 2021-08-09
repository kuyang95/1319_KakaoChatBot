from flask import request, render_template, flash, redirect, url_for, jsonify, Flask
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy # 데이터베이스
from flask_migrate import Migrate

import os
import requests
import json

# 모듈화 파일

# 데이터 베이스
from models import db, migrate, User, guestBook

# 알림 기능
from informationPart import m_corona
from informationPart import m_movie
from informationPart import m_musicChart
from informationPart import m_welcome
from informationPart import m_weather

# 시스템
from systemPart import myPage
from systemPart import signUp
from systemPart import signIn
from systemPart import blockId
from systemPart import attendance
from systemPart import inventory
from systemPart import shop
from systemPart import ranking
from systemPart import sellItem

# 게임
from gamePart import gamePartInfo
from gamePart import beefUp

from minzy import minzy

app = Flask(__name__)

# 데이터베이스 초기화
BASE_DIR = os.path.dirname(__file__)
dbfile = os.path.join(BASE_DIR, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hijoker'

db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)
db.app = app
db.create_all()

@app.route('/', methods=['GET','POST']) # 인덱스 페이지
def index():
      if request.method == 'POST':
            if not request.form['writer'] or \
                  not request.form['text']:
                  flash('입력하지 않은 내용이 있습니다', 'error')
            else:
                  gb = guestBook(request.form['writer'], request.form['text'])
                  db.session.add(gb)
                  db.session.commit()
                  flash('글이 성공적으로 작성되었습니다')
      return render_template('index.html', guestBooks = guestBook.query.all())

@app.route('/welcome', methods=['POST']) # 웰컴블록
def call_welcome_skill():
      res = m_welcome.welcome()
      return jsonify(res)

@app.route('/func_quick', methods=['POST']) # 기능부분 바로가기메뉴
def call_quickmenu():
      res = m_welcome.quick_menu()
      return jsonify(res)

@app.route('/gamePartInfo', methods=['POST']) # 기능부분 바로가기메뉴
def call_gamePartInfo():
      res = gamePartInfo.gamePartInfo()
      return jsonify(res)

@app.route('/weather', methods=['POST']) # 날씨 알림
def call_weather():
      res = m_weather.weather(request.get_json())
      return jsonify(res)

@app.route('/musicChart',methods=['POST']) # 멜론차트 알림
def call_music():
      res = m_musicChart.musicChart()
      return jsonify(res)
      
@app.route('/movies', methods=['POST']) # 영화 알림
def call_movie():
      res = m_movie.movie(request.get_json())
      return jsonify(res)

@app.route('/corona', methods=['POST']) #코로나 알림
def call_corona():
      res = m_corona.corona()
      return jsonify(res)
      
@app.route('/myPage', methods=['POST']) # 마이페이지
def call_myPage():
      res = myPage.myPage(request.get_json())
      return jsonify(res)

@app.route('/signUp', methods=['POST']) # 회원가입
def call_signUp():
      res = signUp.signUp(request.get_json())
      return jsonify(res)

@app.route('/signUp_yes', methods=['POST']) # 회원가입2
def call_signUp_yes():
      res = signUp.signUp_yes(request.get_json())
      return jsonify(res)
      
@app.route('/signIn', methods=['POST']) # 로그인
def call_signIn():
      res = signIn.signIn(request.get_json())
      return jsonify(res)

@app.route('/attendance', methods=['POST']) # 출석체크
def call_attendance():
      res = attendance.attendance(request.get_json())
      return jsonify(res)
      
@app.route('/inventory', methods=['POST']) # 유저 인벤토리 출력
def call_inventory():
      res = inventory.inventory(request.get_json())
      return jsonify(res)

@app.route('/sellItem', methods=['POST']) # 아이템 판매하기
def call_sellItem():
      res = inventory.sellItem(request.get_json())
      return jsonify(res)

@app.route('/sellItem_yes', methods=['POST']) # 아이템 판매하기 확정
def call_sellItem_yes():
      res = inventory.sellItem_yes(request.get_json())
      return jsonify(res)
      
@app.route('/viewItemDescript', methods=['POST']) # 아이템 설명보기
def call_viewItemDescript():
      res = inventory.viewItemDescript(request.get_json())
      return jsonify(res)
      
@app.route('/buyAnEquipment', methods=['POST']) # 상점에서 구입 버튼 클릭시
def call_buyAnEquipment():
      res = shop.buyAnEquipment(request.get_json())
      return jsonify(res)
      
@app.route('/shop', methods=['POST']) # 상점
def call_shop():
      res = shop.shop(request.get_json())
      return jsonify(res)
      
@app.route('/shop_equipment', methods=['POST']) # 장비 상점
def call_shop_equipment():
      res = shop.shop_equipment(request.get_json())
      return jsonify(res)
      
@app.route('/ranking', methods=['POST']) # 랭킹
def call_ranking():
      res = ranking.ranking(request.get_json())
      return jsonify(res)
      
@app.route('/beefUp_select', methods=['POST']) # 강화 게임 장비 선택
def call_beefUp_select():
      res = beefUp.beefUp_select(request.get_json())
      return jsonify(res)
      
@app.route('/beefUp', methods=['POST']) # 강화 게임
def call_beefUp():
      res = beefUp.beefUp(request.get_json())
      return jsonify(res)
      
@app.route('/beefUp_try', methods=['POST']) # 강화 게임 결과
def call_beefUp_try():
      res = beefUp.beefUp_try(request.get_json())
      return jsonify(res)

@app.route('/blockId', methods=['POST']) # 블록아이디 확인용
def call_blockId():
      res = blockId.blockId(request.get_json())
      return jsonify(res)


@app.route('/word_by_situation',methods=['POST']) # 민지 오늘의 말씀
def call_rdw():
      res = minzy.rdw(request.get_json())
      return res
      
@app.route('/first_branch',methods=['POST']) # 민지 오늘의 말씀
def call_first_branch():
      res = minzy.first_branch()
      return res

@app.route('/second_branch',methods=['POST']) # 민지 오늘의 말씀
def call_second_branch():
      res = minzy.second_branch(request.get_json())
      return res
      


if __name__ =="__main__":
      app.run(debug=True,host="0.0.0.0", port=1234)


      
      
