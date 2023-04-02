CREATE TABLE KIO_CART (
    CART_SEQ NUMBER PRIMARY KEY, 
	TEL varchar2(4), 
	GOOD_SEQ     NUMBER default 0, 
	GOOD_PRICE   NUMBER default 0, 
	ORDER_AMOUNT NUMBER default 0, 
	ORDER_PRICE  NUMBER default 0, 
	PAY_GUBUN CHAR(1 BYTE) default '1', 
	REG_DATE DATE default sysdate
   );
 
   CREATE TABLE KIO_GOODS (	
    GOOD_SEQ   NUMBER PRIMARY KEY, 
	GOOD_NAME  VARCHAR2(50), 
	GOOD_IMG   VARCHAR2(100), 
	GOOD_PRICE NUMBER default 0, 
	GOOD_DESC  VARCHAR2(400), 
	REG_DATE   DATE default sysdate
 );
 
 create sequence KIO_CART_SEQ  start with 1 increment by 1 nocache;
 create sequence KIO_GOODS_SEQ start with 1 increment by 1 nocache;


insert into KIO_GOODS (GOOD_SEQ, GOOD_NAME, GOOD_IMG, GOOD_PRICE, GOOD_DESC)
    values(KIO_GOODS_SEQ.NEXTVAL, '아메리카노', '/a/bb.png', 2200, '커피1');
    
insert into KIO_GOODS values(KIO_GOODS_SEQ.NEXTVAL, '아메리카노', '/a/bb.png', 2200, '커피1', SYSDATE);

insert into KIO_GOODS (GOOD_SEQ, GOOD_NAME, GOOD_IMG, GOOD_PRICE, GOOD_DESC)
    values(KIO_GOODS_SEQ.NEXTVAL, '카페라떼', '/a/cc.png', 2500, '커피2');
    
insert into KIO_GOODS (GOOD_SEQ, GOOD_NAME, GOOD_IMG, GOOD_PRICE, GOOD_DESC)
    values(KIO_GOODS_SEQ.NEXTVAL, '카페모카', '/a/dd.png', 3000, '커피3');
    
    
select * from KIO_GOODS;

delete from KIO_GOODS where GOOD_seq = 7;

commit;

insert into KIO_CART (CART_SEQ, TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT, ORDER_PRICE)
    values(KIO_CART_SEQ.NEXTVAL, '1111', 1, 2300, 1, 2300);

select * from KIO_CART;

update KIO_CART set PAY_GUBUN = '1', REG_DATE=SYSDATE where TEL = '1111';



insert into KIO_CART (CART_SEQ, TEL, GOOD_SEQ, GOOD_PRICE, ORDER_AMOUNT, ORDER_PRICE)
    values(KIO_CART_SEQ.NEXTVAL, '2222', 1, (select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=1), 1, (select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=1)*1);
    
    
select GOOD_PRICE from KIO_GOODS where GOOD_SEQ=1;