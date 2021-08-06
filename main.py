from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3 as sql
import mail

app = Flask(__name__)
app.secret_key="password"
emp_password = "12345"
admin_password = "54321"
admin_name = "ADMIN"


@app.route('/')
def render_home():
    return render_template("index.html")

@app.route('/about')
def render_about():
    return render_template("about.html")

@app.route('/index')
def render_index():
    return render_template("index.html")

@app.route('/login')
def render_login():
    return render_template("login.html")

@app.route('/customer_register')
def render_customer_register():
    return render_template("customer_register.html")

@app.route('/customer_menu')
def render_customer_menu():
    return render_template("customer_menu.html")

@app.route('/employee_menu')
def render_employee_menu():
    return render_template("employee_menu.html")

@app.route('/admin_menu')
def render_admin_menu():
    return render_template("admin_menu.html")

@app.route('/add_customer_button', methods=['POST','GET'])
def add_customer_record():
    with sql.connect("grocery.db") as conn:
        c = conn.cursor()

        cst_name = request.form.get("name")
        cst_address = request.form.get("address")
        cst_phone = request.form.get("phone")
        cst_email = request.form.get("email")
        if len(cst_phone) == 10:
            c.execute("""
                        INSERT INTO CUSTOMER(cst_name, cst_address, cst_phone, cst_email) VALUES(?,?,?,?)
                        """, (cst_name, cst_address, cst_phone, cst_email))
            conn.commit()
            flash ("Signed Up Successfully!")
            return render_template("customer_register.html")
        else:
            flash ("Invalid Details")
            return render_template("customer_register.html")

@app.route('/employee_register')
def render_add_employee_page():
    return render_template("employee_register.html")

@app.route('/add_employee_button', methods=['POST','GET'])
def add_employee_record():
    with sql.connect("grocery.db") as conn:
        c = conn.cursor()      
        emp_name = request.form.get("name")
        emp_address = request.form.get("address")
        emp_phone = request.form.get("phone")
        emp_email = request.form.get("email")
        if len(emp_phone) == 10:
            c.execute("""
                        INSERT INTO EMPLOYEE(emp_name, emp_address, emp_phone, emp_email) VALUES(?,?,?,?)
                        """, (emp_name, emp_address, emp_phone, emp_email))
            conn.commit()
            flash ("Signed Up Successfully!")
            return render_template("employee_register.html")
        else:
            flash ("Invalid Details")
            return render_template("employee_register.html")

@app.route('/customer_login_button', methods=['POST','GET'])
def customer_login_button():
    if request.method == "POST":
         user_name = request.form["customer_name"]
         phone = request.form["customer_phone"]
         with sql.connect("grocery.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM CUSTOMER WHERE cst_name=? AND cst_phone=?",(user_name,phone) )
            a=cur.fetchall()
            conn.commit() 
            if len(a)!=0:
                session['CUSTOMER']=phone
                return redirect('/customer_menu')  
            else:
                flash("Incorrect name/password")
                return render_template("login.html")

@app.route('/employee_login_button', methods=['POST','GET'])
def employee_login_button():
    if request.method == "POST":
         user_name = request.form["employee_name"]
         phone = request.form["employee_phone"]
         password = request.form["employee_password"]
         with sql.connect("grocery.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM EMPLOYEE WHERE emp_name=? AND emp_phone=?",(user_name,phone) )
            a=cur.fetchall()
            conn.commit() 
            if len(a)!=0  and password == emp_password :
                    session['EMPLOYEE']=phone
                    return redirect('/employee_menu')  
            else:
                flash("MESSAGE")
                return render_template("login.html")

@app.route('/admin_login_button', methods=['POST','GET'])
def admin_login_button():
    if request.method == "POST":
         user_name = request.form["admin_name"]
         password = request.form["admin_password"]
         with sql.connect("grocery.db") as conn:
            
            if user_name == admin_name  and password == admin_password :
                    return redirect('/admin_menu')  
            else:
                 flash("MESSAGE")
                 return render_template("login.html")

@app.route('/add_store_button', methods=['POST'])
def add_store_record():
    with sql.connect("grocery.db") as conn:
        c = conn.cursor()

        store_name = request.form.get("name")
        store_address = request.form.get("address")
        store_phone = request.form.get("phone")
        c.execute("""
                    INSERT INTO STORE(store_name, store_address, store_phone) VALUES(?,?,?)
                    """, (store_name, store_address, store_phone))
        conn.commit()
        return "Successfully added!"

@app.route('/admin_store_details')
def render_admin_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()

        store_query = c.execute("""SELECT * FROM STORE""").fetchall()
        return render_template("admin_store_details.html",store=store_query)

@app.route('/admin_add_store')
def render_admin_add_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()

        store_query = c.execute("""SELECT * FROM STORE""").fetchall()
        return render_template("admin_add_store.html",store=store_query)

@app.route('/customer_place_order')
def render_customer_place_order():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        store_query = c.execute("""SELECT * FROM STORE""").fetchall()
        return render_template("customer_place_order.html",store=store_query)       

@app.route('/customer_place_button', methods=['POST'])
def render_customer_place_button():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
           
        cst_id = session['CUSTOMER']
        details = request.form.get("order")
        store_id = request.form.get("id")
        payment_type = request.form.get("payment")
        c.execute("""
                    INSERT INTO ORDERS(cst_phone, order_details, store_id) VALUES(?,?,?)
                    """, (cst_id, details, store_id))
        conn.commit()
        c.execute("""
                    INSERT INTO PAYMENT(cst_phone, payment_type) VALUES(?,?)
                    """, (cst_id,payment_type))
        conn.commit()
        return "Order Placed!"

@app.route('/customer_delivery_button', methods=['POST'])
def render_customer_delivery_button():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        del_ratings = request.form.get("rating")
        c.execute(""" UPDATE DELIVERY SET
                    delivery_ratings = ?
                    WHERE cst_phone = ?
                     """,(del_ratings,session['CUSTOMER']))
        conn.commit()
        return "Thank you for rating US"

@app.route('/admin_order_details')
def render_admin_view_orders():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        order_query = c.execute("""SELECT * FROM ORDERS""").fetchall()
        return render_template("admin_order_details.html",orders=order_query)

@app.route('/admin_order_button', methods=['POST'])
def render_admin_order_button():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        cst_no = request.form.get("cst_no")
        emp_no = request.form.get("emp_no")
        status = request.form.get("status")
        price = request.form.get("price")
        pay_stat = request.form.get("pay_stat")
        del_stat = request.form.get("del_stat")
        order_id = request.form.get("order_id")
        c.execute(""" UPDATE ORDERS
                    SET emp_phone = ?,
                    order_status = ?,
                    order_price = ?
                    WHERE order_id = ?
                    """, (emp_no, status, price, order_id))
        conn.commit()
        c.execute(""" UPDATE PAYMENT 
                    SET price = ?,
                    payment_status = ?
                    WHERE cst_phone = ?
                    """,(price, pay_stat, cst_no))
        conn.commit()
        c.execute(""" INSERT INTO DELIVERY(emp_phone, delivery_status, cst_phone) VALUES(?,?,?)
                    """,(emp_no,del_stat,cst_no))

        conn.commit()
        return "Order Updated!"

@app.route('/customer_view_order')
def render_customer_view_order():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        order_query = c.execute("""SELECT * FROM ORDERS 
                                WHERE cst_phone = ?
                                """,(session['CUSTOMER'],)).fetchall()
        return render_template("customer_view_order.html",orders=order_query)

@app.route('/customer_payment_details')
def render_customer_payment_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        payment_query = c.execute("""SELECT * FROM PAYMENT 
                                WHERE cst_phone = ?
                                """,(session['CUSTOMER'],)).fetchall()
        return render_template("customer_payment_details.html",payment=payment_query)

@app.route('/admin_customer_details')
def render_admin_customer_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        cust_query = c.execute("""SELECT * FROM CUSTOMER""").fetchall()
        return render_template("admin_customer_details.html",cust=cust_query)

@app.route('/admin_employee_details')
def render_admin_employee_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        emp_query = c.execute("""SELECT * FROM EMPLOYEE""").fetchall()
        return render_template("admin_employee_details.html",emp=emp_query)

@app.route('/admin_payment_details')
def render_admin_payment_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        payment_query = c.execute("""SELECT * FROM PAYMENT""").fetchall()
        return render_template("admin_payment_details.html",payment=payment_query)

@app.route('/customer_delivery_details')
def render_customer_delivery_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        delivery_query = c.execute("""SELECT * FROM DELIVERY
                                WHERE cst_phone = ?
                                """,(session['CUSTOMER'],)).fetchall()
        return render_template("customer_delivery_details.html",delivery=delivery_query)

@app.route('/admin_delivery_details')
def render_admin_delivery_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        delivery_query = c.execute("""SELECT * FROM DELIVERY""").fetchall()
        return render_template("admin_delivery_details.html",delivery=delivery_query)

@app.route('/employee_search_orders', methods=['POST'])
def render_employee_search_orders():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        val = request.form.get('searchorder')
        order_query = c.execute("""SELECT * FROM  ORDERS
                            WHERE order_id=?
                            """,(val,)).fetchall()
        return render_template("employee_search_orders.html",orders=order_query)

@app.route('/emp_cus_details', methods=['POST'])
def render_emp_cus_details():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        val=request.form.get('cid')
        print(val)
        customer_query = c.execute("""SELECT * FROM CUSTOMER
                                WHERE cst_phone=?
                                """,(val,)).fetchall()
        print(customer_query)
        return render_template("emp_cus_details.html",cust=customer_query)

@app.route('/employee_view_store_details', methods=['POST'])
def render_employee_view_store():
    with sql.connect('grocery.db') as conn:
        c=conn.cursor()
        val=request.form.get('store_id')
        store_query=c.execute("""SELECT * FROM STORE
                            WHERE store_id = ?
                            """,(val,)).fetchall()
        return render_template("employee_view_store_details.html",store=store_query)

@app.route('/employee_finalize_payment',methods=['POST'])
def render_employee_finalize_payment():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        val = request.form.get('cst_no')
        payment_query = c.execute("""SELECT * FROM  PAYMENT
                                WHERE cst_phone=?
                                """,(val,)).fetchall()
        return render_template("employee_finalize_payment.html",payment=payment_query)

@app.route('/employee_payment_final', methods=['POST'])
def render_employee_payment_final():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        pay_stat = request.form.get('pay_stat')
        pay_id = request.form.get("pay_id")
        c.execute(""" UPDATE PAYMENT 
                    SET payment_status = ?
                    WHERE payment_id = ?
                    """,(pay_stat, pay_id))
        conn.commit()
    return "Status Updated!"

@app.route('/employee_finalize_delivery',methods=['POST'])
def render_employee_finalize_delivery():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        val=request.form.get('emp_no')
        delivery_query = c.execute("""SELECT * FROM  DELIVERY
                                WHERE emp_phone=?
                                """,(val,)).fetchall()
        return render_template("employee_finalize_delivery.html",delivery=delivery_query)

@app.route('/employee_deliver_final', methods=['POST'])
def render_employee_deliver_final():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        del_stat = request.form.get("delivery_stat")
        del_id = request.form.get("delivery_id")
        date = request.form.get("date")
        time = request.form.get("time")
        c.execute(""" UPDATE DELIVERY 
                    SET delivery_status = ?,
                    delivery_date = ?,
                    delivery_time = ?
                    WHERE delivery_id = ?
                    """,(del_stat, date, time, del_id))
        conn.commit()
    return "Status Updated!"

@app.route('/delete_stores/<store_id>')
def delete_stores(store_id):
    print("hello")
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM STORE WHERE store_id = (?)""", (store_id,))
        return redirect('/admin_store_details')

@app.route('/delete_delivery/<int:delivery_id>')
def delete_delivery(delivery_id):
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM DELIVERY WHERE delivery_id = (?)""", (delivery_id,))
        return redirect('/admin_delivery_details')

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM ORDERs WHERE order_id = (?)""", (order_id,))
        return redirect('/admin_order_details')

@app.route('/delete_customer/<string:cst_id>')
def delete_customer(cst_id):
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM CUSTOMER WHERE cst_phone =(?)""", (cst_id,))
        return redirect('/admin_customer_details')

@app.route('/delete_employee/<string:emp_id>')
def delete_employee(emp_id):
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM EMPLOYEE WHERE emp_phone = (?)""", (emp_id,))
        return redirect('/admin_employee_details')

@app.route('/delete_payment/<string:pay_id>')
def delete_payment(pay_id):
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM PAYMENT WHERE payment_id = (?)""", (pay_id,))
        return redirect('/admin_payment_details')

@app.route('/send_email', methods=['POST'])
def send_email():
    with sql.connect('grocery.db') as conn:
        c = conn.cursor()
        val=request.form.get("order_id")
        data = c.execute(""" SELECT o.order_id, o.order_details, c.cst_email, c.cst_name, s.store_id, s.store_name,
                         d.delivery_id, d.delivery_date, d.delivery_time,
                         p.payment_type, p.price FROM
                         ORDERS o, DELIVERY d, PAYMENT p, CUSTOMER c, STORE s
                         WHERE o.cst_phone = c.cst_phone AND c.cst_phone = d.cst_phone AND s.store_id = o.store_id 
                         AND c.cst_phone = p.cst_phone AND o.order_id = ?
        """, (val, )).fetchone()
        print(data)
        mail.Send_mail(data)
        return ("Mail sent successfully")
    