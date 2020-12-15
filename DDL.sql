-- TABLE
CREATE TABLE admin  (
   admin_id  VARCHAR,
   admin_name  VARCHAR,
   email_adress  VARCHAR,
   password  VARCHAR,
  PRIMARY KEY ( admin_id )
);
CREATE TABLE banned_writer  (
   writer_id  VARCHAR,
   banned_on  DATE,
   banned_till  DATE,
   num_of_offences  int,
  PRIMARY KEY ( writer_id )
);
CREATE TABLE books  (
   book_id  VARCHAR,
   title  VARCHAR,
   writer_name  VARCHAR,
   writer_id  VARCHAR,
   isbn  VARCHAR(13),
   language  VARCHAR,
   num_pages  int,
   reviews_count  int,
   average_rating  float,
   genre  VARCHAR,
   Price  int,
   summary  VARCHAR,
   book_text  TEXT,
   publishing_id  VARCHAR,
  PRIMARY KEY ( book_id ),
    FOREIGN KEY (writer_id) REFERENCES writer(writer_id)
);
CREATE TABLE credit_card  (
   credit_card_no  VARCHAR,
   cvc  VARCHAR(3),
   expiry_date  DATE,
   balance  int,
  PRIMARY KEY ( credit_card_no )
);
CREATE TABLE customer  (
   customer_id  VARCHAR,
   customers_name  VARCHAR,
   dob  DATE,
   email_adress  VARCHAR,
   Address  VARCHAR,
   password  VARCHAR,
   num_books_owned  int,
   credit_card_no  VARCHAR,
  PRIMARY KEY ( customer_id ),
  FOREIGN KEY (credit_card_no) REFERENCES credit_card(credit_card_no)
);
CREATE TABLE customers_Catalog  (
   customer_id  VARCHAR,
   book_id  VARCHAR,
   order_id  VARCHAR,
  PRIMARY KEY ( customer_id,book_id ),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (book_id,order_id) REFERENCES orders(book_id,order_id)
);
CREATE TABLE orders  (
   order_id  VARCHAR,
   book_id  VARCHAR,
   customer_id  VARCHAR,
   selling_date  DATETIME,
   selling_price  int,
  PRIMARY KEY ( order_id ),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
   FOREIGN KEY (customer_id,book_id) REFERENCES customer_catalog(customer_id,book_id)

  
);
CREATE TABLE promotions  (
   promotion_code  VARCHAR,
   book_id  VARCHAR,
   customer_id  VARCHAR,
   Status  int,
   Percentage  float,
   valid_from  date,
   Till  date,
  PRIMARY KEY ( promotion_code ,  customer_id ,  book_id ),
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
CREATE TABLE reviews  (
   review_id  VARCHAR,
   book_id  VARCHAR,
   review_order  int,
   customer_id  VARCHAR,
   rating  int(1),
   review_text  VARCHAR,
  PRIMARY KEY ( review_id ),
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
  
);
CREATE TABLE shopping_cart  (
   shopping_cart_id  VARCHAR,
   customer_id  VARCHAR,
   book_id  VARCHAR,
   price  int,
   added_on  DATETIME,
  PRIMARY KEY ( shopping_cart_id ),
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
CREATE TABLE writer  (
   writer_id  VARCHAR,
   writer_name  VARCHAR,
   email_adress  VARCHAR,
   address  VARCHAR,
   password  VARCHAR,
   num_books_published  int,
   credit_card_no  VARCHAR,
  PRIMARY KEY ( writer_id ),
  FOREIGN KEY (credit_card_no) REFERENCES credit_card(credit_card_no)

);
CREATE TABLE writers_catalog  (
   writer_id  VARCHAR,
   book_id  VARCHAR,
   publishing_id  VARCHAR,
  PRIMARY KEY ( publishing_id ),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
);
 
-- INDEX
 
-- TRIGGER
 
-- VIEW
 
