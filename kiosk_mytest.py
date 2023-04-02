import cx_Oracle

def good_list():  # -- 상품 목록 출력
    conn = cx_Oracle.connect("ai","0000","localhost:1521/XE")
    cur = conn.cursor()
    sql = "select * from KIO_GOODS"
    cur.execute(sql)
    for row in cur:
        print(list(row))
    cur.close()
    conn.close()

def search_good(parm_seq):  # -- 상품 목록 출력
    conn = cx_Oracle.connect("ai","0000","localhost:1521/XE")
    cur = conn.cursor()
    sql = "select * from KIO_GOODS where GOOD_SEQ = :1"
    cur.execute(sql, [parm_seq])
    # print(list(cur)[0])
    goods_info = list(cur)[0]
    cur.close()
    conn.close()
    return goods_info

def cart_add(parm_tel, parm_seq, parm_amt):
    ginfo = search_good(parm_seq)
    gprice = ginfo[3]

    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    # 줄이 길면 ''' ''' 로 쓰면 multi-line으로 넣을 수 있다.
    sql = '''insert into KIO_CART (CART_SEQ, TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT, ORDER_PRICE)
          values(KIO_CART_SEQ.NEXTVAL, :1, :2, :3, :4, :5)'''
    cur = conn.cursor()
    cur.execute(sql, [parm_tel, parm_seq, gprice, parm_amt, gprice*parm_amt])
    conn.commit()
    cur.close()
    conn.close()

# def cart_add2(parm_tel, parm_seq, parm_amt):
#     conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
#     sql = "insert into KIO_CART (CART_SEQ, TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT, ORDER_PRICE) " \
#           "values(KIO_CART_SEQ.NEXTVAL, :1, :2, " \
#           "(select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=:2), :3, " \
#           "(select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=:2)*:3);"
#     cur = conn.cursor()
#     cur.execute(sql, [parm_tel, parm_seq, parm_amt])
#     conn.commit()
#     cur.close()
#     conn.close()

def orders(parm_tel, pram_gubun):
    "update KIO_CART set PAY_GUBUN = '1', REG_DATE=SYSDATE where TEL = '1111'"
    conn = cx_Oracle.connect("ai", "0000", "localhost:1521/XE")
    sql = "update KIO_CART set PAY_GUBUN = :1, REG_DATE=SYSDATE where TEL = :2"
    cur = conn.cursor()
    cur.execute(sql, [pram_gubun, parm_tel])
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    good_list()
    # cart_add('0142',1,3)
    # cart_add2('4444',1,3)
    # orders('0142', '2')