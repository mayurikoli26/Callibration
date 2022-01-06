import os
from datetime import datetime
from flask import Flask,render_template, request, url_for, session
from flask_mysqldb import MySQL
import re 

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
#app.config['MYSQL_HOST'] = 'aim.cvot3mbu0m9d.us-east-2.rds.amazonaws.com'
#app.config['MYSQL_USER'] = 'gismaster'
#app.config['MYSQL_PASSWORD'] = 'first#1234'

app.config['MYSQL_DB'] = 'calibration'
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index_login.html", message="Hello Flask!");    
    #return render_template("try1.html", message="Hello Flask!", contacts = ['c1', 'c2', 'c3', 'c4', 'c5']);

#All ablut login and session. Takenfrom other site.
@app.route('/login')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s and active=True', (username, password, ))
        account = cursor.fetchone()
        
        print ("account=",account)
        if account:
            #print ("accountID=", account[0])
            session['loggedin'] = True
            #session['id'] = account['id']
            session['session_id'] = account[0]
            #session['username'] = account['username']
            session['username'] = account[1]
            session['role'] = account[4]
            msg = 'Logged in successfully ! Session on'
            if session['role'] in ('admin'):
               return render_template('index_admin.html', msg = msg, session_id=session['session_id'], session_username=session['username'], role=session['role'])
            else:
               return render_template('index_login.html', msg = msg, session_id=session['session_id'], session_username=session['username'], role=session['role'])
        else:
            msg = 'Incorrect username / password !'
    return render_template('login_login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('session_id', None)
    session.pop('username', None)
    #return redirect(url_for('/login'))
    return render_template('login_login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

#manage user profile: user psw, contant no, email, address, User_id(not editable), active, role
@app.route('/profile', methods =['GET', 'POST'])
def profile():
    msg = ''
    errflg= ''
    if request.method == 'POST' and 'username' in request.form :
        username = request.form['username']
        new_psw = request.form['new_psw']
        rep_new_psw = request.form['rep_new_psw']
        old_psw = request.form['old_psw']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        #print("Form contains :",username,old_psw, new_psw, rep_new_psw, account, account[2])
        #print('compare old-psw=',old_psw,' and ',account[2])
        if account:
            msg = 'Account exists !'
            if not re.match(r'[A-Za-z0-9]+', new_psw):
                msg = 'New Password must contain only characters and numbers !'
                errflg = 'error'
            if new_psw != rep_new_psw :
                msg= 'psw and repeat psw should be same !'
                errflg = 'error' 
            if old_psw != account[2] :
                print ('MSG=',old_psw, account[2])
                msg = 'Incorrect current password' 
                errflg = 'error'      
            if errflg:
                print ("error in form.") 
            else:    
                print ("can insert values of new psw")
                msg='Success Change password !'
                #INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
                cursor = mysql.connection.cursor()
                cursor.execute(('UPDATE accounts set password=%s where id = %s'), (new_psw, account[0]))
                mysql.connection.commit()
                
        else:
            msg = 'You should have account registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('changepsw.html', msg = msg)    


# Display all vender list in table
@app.route('/select_vender')
def select_vender():
    if 'session_id' in session:  
        sessionid = session['session_id']
        session_role = session['role']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name, vender_id, address FROM vender")
        data = cursor.fetchall()
        venderid = request.args.get('venderid')
        print ("in vender id= ",venderid)
        if session_role == 'admin':
            return render_template('select_vender.html', data=data, venderid=venderid, role=session_role)
        else:
            return  render_template('select_vender.html', data=data, venderid=venderid, role=session_role)  
    else:  
        return '<p>Please login first</p>' 
    

@app.route('/select_dept')
def select_dept():
    if 'session_id' in session:  
        sessionid = session['session_id'] 
        print ("in dept sessionid= ",sessionid) 
        sel = request.args.get('dept')
        venderid = request.args.get('venderid')
        print ("vender =",venderid)
        cursor = mysql.connection.cursor()
        #cursor.execute("SELECT equ_name, equ_parameter_id  FROM equipment")
        cursor.execute("SELECT department_name, department_id FROM department")
        data = cursor.fetchall()
        return render_template('select_dept.html', data=data, deptid=sel, venderid=venderid)
    else:  
        return '<p>Please login first</p>' 
    #sel = request.args.get('vender')
    #cursor = mysql.connection.cursor()
    #cursor.execute("SELECT department_name, department_id FROM department")
    #data = cursor.fetchall()
    #return render_template('select_dept.html', data=data, venderid=sel)    

@app.route('/select_equip')
def select_equip():
    if 'session_id' in session:  
        sessionid = session['session_id']
        sel = request.args.get('deptid')
        venderid = request.args.get('venderid')
        print ("venderid in eq=", venderid)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT equ_name, equ_parameter_id  FROM equipment")
        data = cursor.fetchall()
        return render_template('select_equip.html', data=data, deptid=sel, venderid=venderid) 
    else:  
        return '<p>Please login first</p>'

# get comma seperated record and show in table
@app.route('/hosplist')
def hosplist():
    equipid = request.args.get('equipment')
    print ("EQP=",equipid)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT parameter_name FROM equ_parameter_reg where equ_parameter_id=%s",(equipid,))
    data = cursor.fetchall()
    s = "-"
    for row in data:
        print(row)  
        s=s.join(row)
        rowx = s.split(',')           

    return render_template('hosplist.html', data=rowx)


@app.route('/parameter_input')
def parameter_input():
    if 'session_id' in session:
       deptid = request.args.get('deptid')
       venderid = request.args.get('venderid')
       equipmentid = request.args.get('equipmentid')
       equ_name = request.args.get('equ_name')
       equ_parameter_id = request.args.get('equ_parameter_id')
       cursor = mysql.connection.cursor()
       
       cursor.execute('SELECT equ_name, equ_parameter_id FROM equipment where equ_id =%s',(equipmentid,))
       print("hi i am id",equipmentid )
       #equ_name = cursor.fetchone()
       data = cursor.fetchall()
       for row in data:
            equ_name = row[0]
            equ_parameter_id = row[1]  #1

       print('EQUIP=',equ_parameter_id)
       cursor.execute("SELECT parameter_name FROM equ_parameter_reg where equ_parameter_id=%s",(equ_parameter_id,))
       data = cursor.fetchall()
       s = "-"
       add_para = ["para1","para2","para3","para4"]
       for row in data:
           print(row)  
           s=s.join(row)
           rowx = s.split(',')           
           return render_template('parameter_input.html', data=rowx, venderid=venderid, deptid=deptid, equipmentid=equipmentid, equ_name=equ_name, add_para=add_para, equ_parameter_id=equ_parameter_id)
    else:  
        return '<p>Please login first.</p>'

@app.route('/last_reading')
def last_reading():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    equipmentid = request.args.get('equipmentid')

    return render_template('last_reading.html' )

@app.route('/previous_reading')
def previous_reading():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    equipmentid = request.args.get('equipmentid')

    return render_template('previous_reading.html' )


@app.route('/add_equipment')
def add_equipment():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    equipmentid = request.args.get('equipmentid')

    return render_template('add_equipment.html' )

    
@app.route('/parameter_list')
def parameter_list():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    equipmentid = request.args.get('equipmentid')


    return render_template('parameter_list.html')


@app.route('/save_reading',methods=['GET', 'POST'])
def save_reading():
    if 'session_id' in session:  
        sessionid = session['session_id']
        if request.method == 'POST' :
            #equipmentid = request.args.get('equipmentid')
            print(request.form)
            print(request.form.to_dict())
            form_obj = request.form.to_dict()
            equipmentid = request.form['equipmentid']
            form_values = request.form['textall']
            remark = request.form['Remarks']
            approvar_name = request.form['approvar_name']
            approvar_email = request.form['approvar_email']
            try :
               verified1 = request.form['verified']
               varified1=0
            except :
                varified1 = 1

            #print ("varified=",verified)
            #if verified != 'on':
            #    verified =0
            #followed = request.form['followed']
            #approvar_email='rajan22@mail.com'

            # Get equ_parameter_id from equipmentid
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT equ_name, equ_parameter_id FROM equipment where equ_id =%s',(equipmentid,))        
            data = cursor.fetchall()
            for row in data:
                equ_name = row[0]
                equ_parameter_id = row[1]
        
            # get parameter_names (list) in array defined from equ_parameter_id
            cursor.execute('SELECT parameter_name FROM equ_parameter_reg where equ_parameter_id =%s',(equ_parameter_id,))
            data = cursor.fetchall()
            for row in data:
                parameter_name = row[0]

            para_name = str(parameter_name)

            # split on | and get a parameter list
            #para_list = form_values.split("|")

            # remove unwanted elements from list
            #del para_list[-8]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[-1]
            #del para_list[2]

            # Again join and get string with | seperated values in string.
            #from_values_m = '|'.join(map(str, para_list)) 
            timestamp=datetime.now()
            cur_date = timestamp.strftime("%Y-%m-%d")
            
            # insert all the values along with (coma seperated) data string (parameter_readings in calibrate).
            #cursor.execute('insert  into calibrate (id, equ_id, parameter_readings, perform_date, approvar_name, remark,approvar_email,digitally_signed ) values (%s,%s,%s, %s, %s, %s,%s,%s)', (sessionid,equipmentid,from_values_m,cur_date, approvar_name, remark,approvar_email,verified1,))
            #mysql.connection.commit()
            cursor.execute('insert  into calibrate (id, equ_id, parameter_readings, perform_date ) values (%s,%s,%s, %s)', (sessionid,equipmentid,form_obj, cur_date,))
            mysql.connection.commit()
            #print ('Parameter=', from_values_m,' Name=',para_list,'Inserted OKLEN=',len(para_list))
            #return "para_name ", parameter_name," Name=",parameter_name
            return  str(form_values)

    else:  
        return '<p>Please login first</p>'

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    calibrate_id ='32'    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT parameter_readings, approvar_name FROM calibrate where calibrate_id =%s',(calibrate_id,)) 
    data = cursor.fetchall()
    for row in data:
        obj_ret = row[0]    
 
    #print  (row[0])
    print (obj_ret)
    return obj_ret            

@app.route('/json_table', methods = ['GET','POST'])
def jason_table():
    return render_template('json_table.html')
     

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True) 



