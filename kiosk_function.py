import cx_Oracle

# --------------------------------------
# 상품목록
# --------------------------------------
def goods_list () :
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = "select * from KIO_GOODS"
    cur = conn.cursor()
    cur.execute(sql)
    for row in cur:
        print(list(row))
    cur.close()
    conn.close()

#--------------------------------------
# 카트담기
#  insert into KIO_CART(CART_SEQ,TEL,GOOD_SEQ,GOOD_PRICE,ORDER_AMOUNT, REG_DATE)
#  values(KIO_CART_SEQ.nextval, '0505', 1, 1000, 2, sysdate);
#--------------------------------------
def search_good(parm_seq):  # -- 상품 목록 출력
    conn = cx_Oracle.connect("ai","0000","localhost:1521/XE")
    cur = conn.cursor()
    sql = "select * from KIO_GOODS where GOOD_SEQ = :1"
    cur.execute(sql, [parm_seq])
    goods_info = list(cur)[0]
    cur.close()
    conn.close()
    return goods_info


def cart_add(parm_tel, parm_seq, parm_amt)  :
    ginfo = search_good(parm_seq)
    gprice = ginfo[3]

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = ''' insert into KIO_CART(CART_SEQ,TEL,GOOD_SEQ,GOOD_PRICE,ORDER_AMOUNT, REG_DATE)
        values(KIO_CART_SEQ.nextval, :1, :2, :3, :4, sysdate)
    '''
    cur = conn.cursor()
    cur.execute(sql, [parm_tel, parm_seq, gprice, parm_amt])
    conn.commit()
    cur.close()
    conn.close()

def cart_add2(TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT)  :
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = '''insert 
             into KIO_CART(CART_SEQ,TEL,GOOD_SEQ,GOOD_PRICE,ORDER_AMOUNT,REG_DATE)
             values(KIO_CART_SEQ.nextval, :1, :2, :3, :4, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT])  #'0505', 1, 1000, 2
    conn.commit()
    cur.close()
    conn.close()

def cart_add3(parm_tel, parm_seq, parm_amt):
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = '''insert into KIO_CART (CART_SEQ, TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT, REG_DATE) 
          values(KIO_CART_SEQ.NEXTVAL, :1, :2, 
          (select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=:3), :4, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [parm_tel, parm_seq, parm_seq, parm_amt])
    conn.commit()
    cur.close()
    conn.close()

# --------------------------------------
# 상품주문
#  insert into kio_order(ORDER_SEQ,TEL,ORDER_PRICE,PAY_GUBUN,REG_DATE)
#  values (kio_order_seq.nextval, '0505',  4500, '1', sysdate);
# --------------------------------------
def get_totalprice(parm_tel):
    conn = cx_Oracle.connect("ai","0000","localhost:1521/XE")
    cur = conn.cursor()
    sql = '''select sum(good_price*order_amount) from KIO_CART where tel=:1'''
    cur.execute(sql, [parm_tel])
    goods_info = list(cur)[0]
    cur.close()
    conn.close()
    return goods_info

def orders(parm_tel, pram_gubun):
    totprice = get_totalprice(parm_tel)[0]

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = ''' insert into kio_order(ORDER_SEQ,TEL,ORDER_PRICE,PAY_GUBUN,REG_DATE)
            values (kio_order_seq.nextval, :1,  :2, :3, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [parm_tel, totprice, pram_gubun])
    conn.commit()
    cur.close()
    conn.close()

def orders2(TEL,ORDER_PRICE,PAY_GUBUN):
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = ''' insert into kio_order(ORDER_SEQ,TEL,ORDER_PRICE,PAY_GUBUN,REG_DATE)
              values (kio_order_seq.nextval, :1, :2, :3, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [TEL,ORDER_PRICE,PAY_GUBUN])  #'0505',  4500, '1'
    conn.commit()
    cur.close()
    conn.close()

def orders3(parm_tel, pram_gubun):
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = ''' insert into kio_order(ORDER_SEQ,TEL,ORDER_PRICE,PAY_GUBUN,REG_DATE)
            values (kio_order_seq.nextval, :1,  
            (select sum(good_price*order_amount) from KIO_CART where tel=:2),
             :3, sysdate)'''
    cur = conn.cursor()
    cur.execute(sql, [parm_tel, parm_tel, pram_gubun])
    conn.commit()
    cur.close()
    conn.close()

def order_list(parm_orderid):
    temp_list = []
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = ''' select o.order_seq, o.tel, g.good_seq, g.GOOD_NAME, g.GOOD_PRICE, c.ORDER_AMOUNT, o.ORDER_PRICE
             from KIO_ORDER o, KIO_CART c, KIO_GOODS g
             where c.tel = o.tel
             and c.good_seq = g.good_seq
             and o.order_seq = :1
            '''
    cur = conn.cursor()
    cur.execute(sql, [parm_orderid])
    for row in cur:
        temp_list.append(list(row))
    cur.close()
    conn.close()

    for i, row in enumerate(temp_list):
        if i == 0:
            print("order id:", row[0], "tel:", row[1])
        print("good id:", row[2], "good name:", row[3], "good price:", row[4], "amount:", row[5])
    print("total price:", row[-1])

    return temp_list

if __name__ == '__main__':
    # goods_list()
    # cart_add('0142',1,3)
    # cart_add2('0505', 1, 1000, 2)
    # cart_add3('5555', 1, 2)

    # orders('0505', '1')
    # orders2('0505', 4500, '1')

    # info = get_totalprice("0505")
    # print(info)

    # orders3('0505', '2')

    temp_list = order_list(1)