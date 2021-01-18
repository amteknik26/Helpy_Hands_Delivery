import sqlite3;

def init_db():
    with sqlite3.connect("grocery.db") as conn:
        c = conn.cursor()

        #CUSTOMER TABLE
        c.execute("""
                    CREATE TABLE IF NOT EXISTS CUSTOMER(
                        cst_name TEXT,
                        cst_address TEXT,
                        cst_phone TEXT PRIMARY KEY,
                        cst_email TEXT
                    );    
                """)
        conn.commit()

        #EMPLOYEE TABLE
        c.execute("""
                    CREATE TABLE IF NOT EXISTS EMPLOYEE(
                        emp_name TEXT,
                        emp_address TEXT,
                        emp_phone TEXT PRIMARY KEY,
                        emp_email TEXT
                    );    
                """)
        conn.commit()

        #STORE TABLE
        c.execute("""
                    CREATE TABLE IF NOT EXISTS STORE(
                        store_id INTEGER PRIMARY KEY,
                        store_name TEXT,
                        store_address TEXT,
                        store_phone TEXT
                    );    
                """)
        conn.commit()

        #ORDER TABLE
        c.execute("""
                    CREATE TABLE IF NOT EXISTS ORDERS(
                        cst_phone TEXT,
                        emp_phone TEXT,
                        store_id INTEGER,
                        order_id INTEGER PRIMARY KEY,
                        order_details TEXT,
                        order_status INTEGER,
                        order_price INTEGER,
                        FOREIGN KEY(cst_phone) REFERENCES CUSTOMER(cst_phone) ON DELETE CASCADE,
                        FOREIGN KEY(emp_phone) REFERENCES EMPLOYEE(emp_phone) ON DELETE CASCADE,
                        FOREIGN KEY(store_id) REFERENCES STORE(store_id) ON DELETE CASCADE
                    );    
                """)
        conn.commit()
        
        #DELIVERY TABLE
        c.execute("""
                    CREATE TABLE IF NOT EXISTS DELIVERY(
                        emp_phone TEXT,
                        cst_phone TEXT,
                        delivery_id INTEGER PRIMARY KEY,
                        delivery_date TEXT,
                        delivery_time TEXT,
                        delivery_status INTEGER,
                        delivery_ratings INTEGER,
                        FOREIGN KEY(cst_phone) REFERENCES CUSTOMER(cst_phone) ON DELETE CASCADE,
                        FOREIGN KEY(emp_phone) REFERENCES EMPLOYEE(emp_phone) ON DELETE CASCADE
                    );    
                """)
        conn.commit()

        #PAYMENT TABLE
        c.execute("""
                    CREATE TABLE IF NOT EXISTS PAYMENT(
                        cst_phone TEXT,
                        payment_id INTEGER PRIMARY KEY,
                        payment_type TEXT,
                        price INTEGER,
                        payment_status INTEGER,
                        FOREIGN KEY (cst_phone) REFERENCES CUSTOMER (cst_phone) ON DELETE CASCADE
                    );    
                """)
        conn.commit()

        


init_db()