from flask import Flask, render_template, request, url_for, flash, redirect, session

#Get JSON response
from psycopg2.extras import RealDictCursor
# cur = conn.cursor(cursor_factory=RealDictCursor)

import psycopg2
import os
import hashlib

app = Flask(__name__)
app.secret_key = "super secret key"

#SALT for security
salt = "imyapp12348007670555createdinpune15082023-hluvdelhi4ever-1274-96"

def db_conn_creation():
    return psycopg2.connect(
        host="dietician_postgres",
        database="postgres",
        user="admin",
        password="secret")
        
def PasswordValidate(username,password,type):
    password_rd = hashlib.md5()
    val_pass = username+salt+password
    password_rd.update(val_pass.encode('utf-8'))
    md5_hex = password_rd.hexdigest()
    if type == 'create':
      return md5_hex
    query = "select username from user_db where usr_id ='"+md5_hex+"'"
    conn = db_conn_creation()
    with conn.cursor() as cur:
        cur.execute(query)
        row = cur.fetchall()
        app.logger.info(row[0][0])
    conn.close()
    if row[0][0] == username:
        app.logger.info('found the ID')
        return True
    else:
        app.logger.info("no such ID present")
        return False

@app.route('/create_user/', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        login_user_id = request.form['username']
        user_password = request.form['password']
        user_password_cnf = request.form['password_cnf']
        hex_val = PasswordValidate(login_user_id,user_password,'create')
        add_user_query = """insert into user_db (usr_id, username) values ('{}','{}')""".format(hex_val,login_user_id)
        app.logger.info(add_user_query)
        add_diet_query = """insert into product_db (usr_id, username) values ('{}','{}')""".format(hex_val,login_user_id)
        app.logger.info(add_diet_query)

        if not login_user_id:
            flash('username is required!')
        elif not user_password:
            flash('password is required!')
        elif not user_password_cnf:
            flash('please confirm password!')
        elif user_password != user_password_cnf:
            flash('password doesn\'t match!')
        else:
            app.logger.info("connection is being created")
            conn = db_conn_creation()
            with conn.cursor() as cur:
                cur.execute(add_user_query)
                app.logger.info("query executed")
                cur.execute(add_diet_query)
                app.logger.info("query executed")
            conn.commit()
            conn.close()
            flash('login successfully created!')
            return redirect(url_for('login'))#,login_user_id=login_user_id))
    return render_template('create_user.html')

@app.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login_user_id = request.form['username']
        user_password = request.form['password']
        app.logger.info('retrieved the IDs')
        if not login_user_id:
            flash('username is required!')
        elif not user_password:
            flash('password is required!')
        elif PasswordValidate(login_user_id,user_password,'abcd'):
            session["user"] = login_user_id
            flash('Logged in successfully!')
            return redirect(url_for('products'))#,login_user_id=login_user_id))
    return render_template('login.html')
    
@app.route('/products/', methods=('GET','POST'))
def products():
    if session.get('user') == None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        conn = db_conn_creation()
        row = ""
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM PUBLIC.product_db where username = '{}'".format(session.get('user')))
            out = cur.fetchall()
        conn.close()
        dict_prod = [{k:v for k,v in dict(row).items()} for row in out]
        
        return render_template('products.html',catalog = dict_prod)
    return redirect(url_for('login'))

@app.route('/admin/', methods=('GET', 'POST'))
def seller():
    if request.method == 'GET':
        conn = db_conn_creation()
        row = ""
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM PUBLIC.product_db")
            out = cur.fetchall()
        conn.close()
        dict_prod = [{k:v for k,v in dict(row).items()} for row in out]
        print(dict_prod)
        return render_template('admin.html',catalog = dict_prod)
    if request.method == 'POST':
        flash('DB updated!')
        return redirect(url_for('admin'))
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
    
    
'''

# """<!DOCTYPE html>

# <html lang="en">
# <head>
    # <meta charset="UTF-8">
    # <title>Flask Docker</title>
# </head>
# <body>
    # <h1>DataBase Connection Established</h1>
    # <h2>connected to server: {}</h1>
    # <h3>The database name : {}</h1>
# </body>
# </html>""".format("postgres_container","postgres_db")

# Create a new table
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE items (
            id serial PRIMARY KEY,
            name VARCHAR NOT NULL,
            price INT
        )
    """)
conn.commit()

# Insert data
with conn.cursor() as cur:
    cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", ("iPhone 12", 77000))
    cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", ("Portronics Sound Pro II", 15000))
conn.commit()

# Query data
with conn.cursor() as cur:
    cur.execute("SELECT id, name, price FROM items")
    rows = cur.fetchall()
    for row in rows:
        print("ID:", row[0])
        print("Name:", row[1])
        print("Age:", row[2])

# Close the connection
conn.close()



conn = db_conn_creation()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE items (
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL,
                price INT
            )
        """)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", ("iPhone 12", 77000))
        cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", ("Portronics Sound Pro II", 15000))
    conn.commit()
    row = ""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, price FROM items")
        row = cur.fetchall()
    conn.close()
'''