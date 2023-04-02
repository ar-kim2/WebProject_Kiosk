# pip install Flask, requests

from flask import Flask, make_response, jsonify, request, render_template, redirect
import cx_Oracle
# Flask: Python으로 개발가능한 웹 프레임워크
#   이 경우 웹서비스 구동을 위한 통신 등의 뼈대가 이미 만들어져 있다.
#   제공하는 뼈대에 특정 cmd가 오면 특정 동작을 한다 정도만 구현하면 됨.
# 프레임워크: 무언가를 만들기 위한 기본적인 뼈대, 구조

#
#
# 실행하면, 그걸 Python이 아니라 flask에게 넘겨서
# flask가 실행하도록 해줘라 라는 의미
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)와 결합되어서...
app = Flask(__name__)

# Flask를 처음 시작하면 호출하는 함수

tel_num = 1234

@app.route('/')
def index():
    # html을 넣은 때, ./templates/index.html 이렇게 안쓰고
    # index.html만 써도 Flask가 자동으로 template내에서 가져옴.
    goods_list_dict = []

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = "select * from KIO_GOODS"
    cur = conn.cursor()

    cur.execute(sql)
    for row in cur:
        # print(list(row))
        goods_list_dict.append({"GOOD_SEQ":row[0],"GOOD_NAME": row[1], "GOOD_IMG":row[2],"GOOD_PRICE":row[3], "GOOD_DESC":row[4]})
    cur.close()
    conn.close()

    return render_template('index.html', KEY_GOODS_LIST_DIC = goods_list_dict)
    return render_template('index.html')

@app.route('/list')
def test_list():
    test_list = [1,2,3]
    test_dic= {"uid":"kim", "upw":"111"}
    test_list_dic = [{"uid":"kim1", "upw":"555"},
                     {"uid": "kim2", "upw": "666"}]
    return render_template('test.html',
                           KEY_TEST_LIST=test_list,
                           KEY_TEST_DIC = test_dic,
                           KEY_TEST_LIST_DIC = test_list_dic)

@app.route('/detail_view', methods=['POST', 'GET'])
def detail_view():
    parm_goods_seq = ""
    if request.method == 'GET':

        prm_good_seq = request.args.get('prm_good_seq')

        print("\n\nGOOD SEQ 가져옴", prm_good_seq, "\n\n")
    print("상세보기")
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = """  select GOOD_SEQ,GOOD_NAME,GOOD_IMG,GOOD_PRICE,GOOD_DESC
                    from kio_goods
                    where good_seq= :1"""
    cur = conn.cursor()
    cur.execute(sql, [prm_good_seq])
    goods_list_dict = []
    for row in cur:
        # [3, 'CRISPY CHICKEN', 'static/images/menu/burger-11.jpg', 11, 'Chicken breast, chilli sauce, tomatoes, pickles, coleslaw']
        dic = {}
        dic["GOOD_SEQ"] = row[0]
        dic["GOOD_NAME"] = row[1]
        dic["GOOD_IMG"] = row[2]
        dic["GOOD_PRICE"] = row[3]
        dic["GOOD_DESC"] = row[4]
        goods_list_dict.append(dic)
    cur.close()
    conn.close()
    print(goods_list_dict)

    return render_template('product-single.html', KEY_GOODS_LIST_DIC = goods_list_dict)


@app.route('/add_cart', methods=['POST', 'GET'])
def add_cart():
    print("카트담기")
    parm_seq = request.args.get('prm_good_seq')
    parm_amt = request.args.get('parm_amount')
    print("\n\n\n prm_good_seq ", parm_seq, parm_amt,"\n\n")

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = '''insert into KIO_CART (CART_SEQ, TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT, REG_DATE) 
          values(KIO_CART_SEQ.NEXTVAL, :1, :2, 
          (select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=:3), :4, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [tel_num, parm_seq, parm_seq, parm_amt])
    conn.commit()
    cur.close()
    conn.close()

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = '''    select g.GOOD_SEQ, g.GOOD_NAME, g.GOOD_IMG, g.GOOD_DESC,
                c.GOOD_PRICE,  c.ORDER_AMOUNT,  (c.GOOD_PRICE*c.ORDER_AMOUNT) as TOTPRICE
            from KIO_GOODS g,  KIO_CART c
            where g.GOOD_SEQ = c.GOOD_SEQ
                  and TEL = :1'''
    cur = conn.cursor()
    cur.execute(sql, [tel_num])
    goods_list_dict = []
    total_price = 0
    for row in cur:
        # [3, 'CRISPY CHICKEN', 'static/images/menu/burger-11.jpg', 11, 'Chicken breast, chilli sauce, tomatoes, pickles, coleslaw']
        dic = {}
        dic["GOOD_SEQ"] = row[0]
        dic["GOOD_NAME"] = row[1]
        dic["GOOD_IMG"] = row[2]
        dic["GOOD_DESC"] = row[3]
        dic["GOOD_PRICE"] = row[4]
        dic["ORDER_AMOUNT"] = row[5]
        dic["TOTPRICE"] = row[6]
        total_price += int(row[6])
        goods_list_dict.append(dic)
    cur.close()
    conn.close()

    print(goods_list_dict)

    return render_template('cart.html', KEY_GOODS_LIST_DIC=goods_list_dict, KEY_TOTVAL = total_price, TEL_NUM = tel_num)

@app.route('/orders')
def orders():
    global tel_num
    print("주문완료")

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = ''' insert into kio_order(ORDER_SEQ,TEL,ORDER_PRICE,PAY_GUBUN,REG_DATE)
            values (kio_order_seq.nextval, :1,  
            (select sum(good_price*order_amount) from KIO_CART where tel=:2),
             :3, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [tel_num, tel_num, '1'])
    conn.commit()
    cur.close()
    conn.close()

    tel_num = tel_num+1

    return redirect("/")

if __name__ == '__main__':
    # 웹서비스 기본 포트 번호는 80
    # 보통 웹페이지, 첫 진입 페이지는 index.html
    # Flask가 웹서버를 띄우고 기다림.
    # 처음시작하면, localhost:80/ 로 들어감.
    app.debug = True # 개발자 모드, 코드를 수정하면 자동 restart

    # app.run(host='0.0.0.0', port=80)
    app.run(host='localhost', port=80)

    # Flask가 이미 받은 웹페이지 디자인을 인식하게 하려면
    # 오타 없이 무조건 동일 디렉토리 경로에 static, templates 폴더를 만들어야함.
    # 폴더들은 static에 html파일들은 template 파일에 넣는다.


    # Flask는 동정인 동작이라던가 페이지 내에서 애니메이션처럼 보이는 것들은 static에 넣는다.
    # 디자인 관련 html은 templates에 넣는다.