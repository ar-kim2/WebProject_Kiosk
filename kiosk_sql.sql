drop table KIO_CART;
drop table KIO_ORDER;
drop table KIO_GOODS;

drop sequence KIO_CART_SEQ;
drop sequence KIO_GOODS_SEQ;
drop sequence KIO_ORDER_SEQ;

CREATE TABLE KIO_GOODS (
    GOOD_SEQ   NUMBER PRIMARY KEY,
	GOOD_NAME  VARCHAR2(50),
	GOOD_IMG   VARCHAR2(100),
	GOOD_PRICE NUMBER default 0,
	GOOD_DESC  VARCHAR2(400),
	REG_DATE   DATE default sysdate
 );


CREATE TABLE KIO_CART (
    CART_SEQ NUMBER PRIMARY KEY,
	TEL varchar2(4),
	GOOD_SEQ     NUMBER default 0,
	GOOD_PRICE   NUMBER default 0,
	ORDER_AMOUNT NUMBER default 0,
    REG_DATE DATE default sysdate ,
    constraint "FK"  FOREIGN KEY ("GOOD_SEQ")  REFERENCES KIO_GOODS(GOOD_SEQ)
   );

CREATE TABLE KIO_ORDER (
    ORDER_SEQ NUMBER PRIMARY KEY,
	TEL varchar2(4),
    ORDER_PRICE  NUMBER default 0,
	PAY_GUBUN CHAR(1 BYTE) default '1',
	REG_DATE DATE default sysdate
);


 create sequence KIO_CART_SEQ  start with 1 increment by 1 nocache;
 create sequence KIO_GOODS_SEQ start with 1 increment by 1 nocache;
 create sequence KIO_ORDER_SEQ start with 1 increment by 1 nocache;


 insert into KIO_GOODS(GOOD_SEQ,GOOD_NAME,GOOD_IMG,GOOD_PRICE,GOOD_DESC,REG_DATE)
 values (KIO_GOODS_SEQ.nextval, '아메리카노', './img/americano.jpg', 1000, '이건 설명', sysdate);

 insert into KIO_GOODS(GOOD_SEQ,GOOD_NAME,GOOD_IMG,GOOD_PRICE,GOOD_DESC,REG_DATE)
 values (KIO_GOODS_SEQ.nextval, '카페라떼', './img/latte.jpg', 2500, '이건 설명222', sysdate);


 insert into KIO_CART(CART_SEQ,TEL,GOOD_SEQ,GOOD_PRICE,ORDER_AMOUNT, REG_DATE)
 values(KIO_CART_SEQ.nextval, '0505', 1, 1000, 2, sysdate);

  insert into KIO_CART(CART_SEQ,TEL,GOOD_SEQ,GOOD_PRICE,ORDER_AMOUNT, REG_DATE)
 values(KIO_CART_SEQ.nextval, '0505', 2, 2500, 3, sysdate);

 insert into kio_order(ORDER_SEQ,TEL,ORDER_PRICE,PAY_GUBUN,REG_DATE)
 values (kio_order_seq.nextval, '0505',  4500, '1', sysdate);

 commit;

 select * from KIO_CART;

 select * from KIO_GOODS;
 
 select * from kio_order;
 
 select sum(mul_price)
 from(select good_price*order_amount as mul_price from KIO_CART
 where tel = '0505');
 
select * 
 from KIO_ORDER o, KIO_CART c, KIO_GOODS g
 where c.tel = o.tel
 and c.good_seq = g.good_seq;