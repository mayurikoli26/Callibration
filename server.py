import os
from datetime import datetime
from flask import Flask,render_template, request, url_for, session ,jsonify
from flask_mysqldb import MySQL
import re 

import psycopg2 #pip install psycopg2 
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
#app.config['MYSQL_HOST'] = 'aimdb.ccuhjxtwycfp.us-east-1.rds.amazonaws.com'
#app.config['MYSQL_USER'] = 'aimuser'
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
        #print ("account=",account)
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
            #cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            cursor.execute('INSERT INTO accounts (username, password, email, role, active) VALUES ( %s, %s, %s,%s,%s)', (username, password, email,"user",True ))
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
                #print ('MSG=',old_psw, account[2])
                msg = 'Incorrect current password' 
                errflg = 'error'      
            if errflg:
                print ("error in form.") 
            else:
                msg='Success Change password !'
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
        #print ("in vender id= ",venderid)
        if session_role == 'admin':
            return render_template('select_vender.html', data=data, venderid=venderid, role=session_role)
        else:
            return  render_template('select_vender.html', data=data, venderid=venderid, role=session_role)  
    else:  
        return '<p>Please login first</p>' 
    

@app.route('/select_dept', methods =['GET', 'POST'])
def select_dept():
    if 'session_id' in session:  
        sessionid = session['session_id'] 
        #print ("in dept sessionid= ",sessionid)
        sel=1
        venderid = request.form['venderid']
        #print ("vender =",venderid)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT department_name, department_id FROM department where vender_id=%s",(venderid,))
        data = cursor.fetchall()
        #print("venderid im in dept",venderid)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name, vender_id, address FROM vender where vender_id=%s',(venderid,))
        data1 = cursor.fetchall()
        for row in data1:
          name = row[0]
          vender_id =row[1]
          address = row[2]
        return render_template('select_dept.html', data=data, venderid=venderid,name=name)
    else:  
        return '<p>Please login first</p>' 


@app.route('/select_equip', methods =['GET', 'POST'])
def select_equip():
    if 'session_id' in session:  
        sessionid = session['session_id']
        #sel = request.args.get('deptid')
        deptid = request.form['deptid']
      
        venderid = request.form['venderid']
        #print ("venderid in eq=", venderid)
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT name FROM vender where vender_id=%s',(venderid,))
        data = cursor.fetchall()
        for row in data:
          name = row[0]

        cursor.execute('SELECT department_name FROM department where vender_id=%s',(venderid,))
        data = cursor.fetchall()
        for row in data:
          department_name = row[0]  

        cursor.execute("SELECT equ_name, equ_id,equ_asset,equ_model,equ_serialno FROM equipment")
        data = cursor.fetchall()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT equ_parameter_id ,parameter_list, parameter_name FROM parameter")
        data4 = cursor.fetchall()
        #print("data4----------",data4)
        return render_template('select_equip.html', data=data, deptid=deptid, venderid=venderid,name=name, department_name=department_name, data4=data4) 
       
    else:  
        return '<p>Please login first</p>'

# get comma seperated record and show in table
@app.route('/hosplist')
def hosplist():
    equipid = request.args.get('equipment')
    #print ("EQP=",equipid)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT parameter_name FROM parameter where equ_parameter_id=%s",(equipid,))
    data = cursor.fetchall()
    s = "-"
    for row in data:
        #print(row)  
        s=s.join(row)
        rowx = s.split(',')           

    return render_template('hosplist.html', data=rowx)


@app.route('/parameter_input', methods =['GET', 'POST'])
def parameter_input():

    #print("--------------------", request.form)
    if 'session_id' in session:
       deptid = request.form['deptid']  
       venderid = request.form['venderid']
       equipmentid = request.form ['equipmentid']
       equ_name = request.args.get('equ_name')
       equ_parameter_id = request.args.get('equ_parameter_id')
       cursor = mysql.connection.cursor()
       cursor.execute('SELECT equ_name, equ_parameter_id FROM equipment where equ_id =%s',(equipmentid,))
       #equ_name = cursor.fetchone()
       data = cursor.fetchall()
       for row in data:
            equ_name = row[0]
            equ_parameter_id = row[1]  
       
       #cursor.execute("SELECT parameter_name FROM equ_parameter_reg where equ_parameter_id=%s",(equ_parameter_id,))
       cursor.execute("SELECT parameter_list FROM parameter where equ_parameter_id=%s",(equ_parameter_id,))
       data = cursor.fetchall()
       s = "-"
       #print("hi i am EQUE0=",data )            
       #add_para = ["para1","para2","para3","para4"]
       for row in data:
           #print("ROW:",row)  
           s=s.join(row)
           rowx = s.split(',') 
           #print("hi i am EQUE1=",equipmentid )             
           return render_template('parameter_input.html', data=rowx, venderid=venderid, deptid=deptid, equipmentid=equipmentid, equ_name=equ_name, equ_parameter_id=equ_parameter_id)
    else:  
        return '<p>Please login first.</p>'

@app.route('/equipment_details', methods =['GET', 'POST'])
def equipment_details():
    deptid = request.form ['deptid']
    venderid = request.form['venderid']
    equipmentid = request.form['equipmentid']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, vender_id, address FROM vender where vender_id=%s",(venderid,))
    data1 = cursor.fetchall()
    # print("data1",data1)
    for row in data1:
        name = row[0]
        vender_id =row[1]
        address = row[2]
    cursor.execute("SELECT department_name, department_id FROM department where department_id=%s",(deptid,))
    data2 = cursor.fetchall()
    venderid = request.form['venderid']
    for row in data2:
        department_name = row[0]
        department_id =row[1]  
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT equ_name, equ_make,equ_model,equ_serialno,equ_asset,start_date,active FROM equipment where equ_id=%s",(equipmentid,))
    data3 = cursor.fetchall()
    for row in data3:
        equ_name = row[0]
        equ_make  =  row[1]
        equ_model=  row[2]
        equ_serialno =row[3]
        equ_asset =row[4]
        start_date = row[5]
        active =row[6]
    return render_template('equipment_details.html',deptid=deptid, equipmentid=equipmentid, venderid=venderid,name=name,department_name=department_name,equ_name=equ_name,equ_make=equ_make,equ_model=equ_model,equ_serialno=equ_serialno,equ_asset=equ_asset,start_date=start_date,active=active)
  


@app.route('/previous_reading' ,methods =['GET', 'POST'])
def previous_reading():
    deptid = request.form['deptid']
    venderid = request.form['venderid']
    equipmentid = request.form ['equipmentid']
    cursor = mysql.connection.cursor()
    cursor.execute("select equ_name from equipment where equ_id=%s", (equipmentid,))
    eq_name = cursor.fetchall()
    for row in eq_name :
        equ_name=row[0]

    #equ_name ="Myname"
    # cursor.execute("SELECT calibrate_id, perform_date, parameter_readings FROM calibrate where equ_id=%s order by perform_date desc limit 1",(equipmentid,))
    cursor.execute("SELECT parameter_readings FROM calibrate where equ_id=%s",(equipmentid,))
    c = cursor.fetchone()

    cursor.execute("SELECT calibrate_id, perform_date, parameter_readings FROM calibrate where equ_id=%s",(equipmentid,))
    data = cursor.fetchall()
    ##print("data of calibrate",data)
   
    if c is None:
        #print("prev---",c)
        return("No record found. Select other equipment")

    # print ('DATA========== ',equipmentid, deptid, venderid, data)
    for row in data:
    #     calibrate_id = row[0]
          perform_date =  row[1]
          parameter_readings = row[2]
          parameter_readings = parameter_readings.replace("{","")
          parameter_readings = parameter_readings.replace("}","")
    #print ('PREREAD', parameter_readings)
    row = parameter_readings.replace(":",",")
    row = row.replace("'","")
    # rowx = row.split(',')
    rowx= re.split('; |, |\*|\n',row)
    lenrow = len(rowx)/2
    lenrowint = int(lenrow)
    #print ("len of para ",lenrowint)
    return render_template('previous_reading_n.html',deptid=deptid, lenrow=lenrowint, equipmentid=equipmentid, venderid=venderid, perform_date=perform_date, parameter_readings = rowx, data=data, equ_name=equ_name )
     

@app.route('/search' ,methods =['GET', 'POST'])
def search():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    equipmentid = request.args.get('equipmentid')  
    return render_template('search.html')
          
@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    data= request.args.get('q')
    #print("q is",data)
    cursor = mysql.connection.cursor()
    # cursor.execute("select equ_name  from equipment".format(data))#This is just exampel query , you should replace it with your query
    # cursor.execute("SELECT equ_name,equ_id,equ_model, equ_serialno FROM equipment where equ_name=%s",(data,)) 
    cursor.execute("SELECT equ_name, equ_id, equ_model, equ_serialno FROM equipment where equ_name LIKE %s ",[data + "%"])
    result = cursor.fetchall()
    str='<table border= "2" style = ""width=50%">'
    for row in result :
        equ_name = '<td>'+row[0]+'</td>'
        equ_id  = '<td>'+row[1]+'</td>' 
        equ_model='<td>'+row[2]+'</td>'
        equ_serialno ='<td>'+row[3]+'</td>'
        str=str + '<tr>' +equ_name+ '  '+equ_id+" "+equ_model+'  '+ equ_serialno + '</tr>'
        #print("STR-" ,str)
        return ( data+ str)

    #print("query is" ,result )
    str = str + '</table>'
    return (data,result)
 
     
@app.route("/select_e",methods=["GET"])
def select_e():
    # deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    # equipmentid = request.args.get('equipmentid')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT equ_id,equ_name,equ_make,equ_model,equ_serialno,equ_asset,start_date, active FROM equipment where vender_id=%s',(venderid))
    result = cursor.fetchall()
    return jsonify(result= result) 


@app.route("/get_page",methods=["GET"])
def get_page():
    return render_template('select_equip.html')


@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():

    deptid = request.form['deptid']
    venderid = request.form['venderid']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, vender_id, address FROM vender")
    data1 = cursor.fetchall()
    #print(data1)  
    cursor.execute("SELECT department_name, department_id FROM department")
    data2 = cursor.fetchall()
    #print(data2)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT equ_name, equ_id  FROM equipment")
    data3 = cursor.fetchall()
    #print(data3)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT equ_parameter_id ,parameter_list, parameter_name FROM parameter")
    data4 = cursor.fetchall()
    #print("data4----------",data4)
    return render_template('add_equipment.html',deptid=deptid, venderid=venderid, data1=data1, data2=data2, data3=data3, data4=data4)
    

@app.route('/save_new_equipment', methods =['GET', 'POST'])
def save_new_equipment():
    #print ("hello")
    if request.method == 'POST': 
        #print("stage 1")
        form_obj = request.form.to_dict()
        venderid = request.form['venderid']
        #print("venderid",venderid)
        deptid = request.form['deptid']
        #print("deptid",deptid)
        equ_name =request.form['equ_name']
        #print("equ_name",equ_name)
        asset_cd = request.form['asset_cd']
        #print("asset_cd",asset_cd)
        equ_make =request.form['equ_make']
        #print("equ_make",equ_make)
        equ_model =request.form['equ_model']
        #print("equ_model",equ_model)
        serialno = request.form['serialno']
        equ_parameter_id = request.form['equ_parameter_id']
        #print("   equ_parameter_id======",   equ_parameter_id)
        form_values = request.form['textall']
        #print("form_value",form_values )
        timestamp=datetime.now()
        cur_date=timestamp.strftime("%Y-%m-%d")
        cursor = mysql.connection.cursor()
        #cursor.execute('insert  into calibrate (id, equ_id, parameter_readings, perform_date ) values (%s,%s,%s, %s)', (sessionid,equipmentid,form_obj, cur_date,))
        cursor.execute('insert  into equipment (vender_id,department_id,equ_name,equ_asset,equ_make,equ_model,equ_serialno,equ_parameter_id, start_date) values (%s, %s, %s,%s,%s,%s,%s,%s,%s)', (venderid,deptid,equ_name,asset_cd,equ_make,equ_model,serialno,equ_parameter_id,cur_date))
        mysql.connection.commit()  
        cursor.execute("SELECT department_name, department_id FROM department where vender_id=%s",(venderid,))
        data = cursor.fetchall()
        #print("venderid im in dept",venderid)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name, vender_id, address FROM vender where vender_id=%s',(venderid,))
        data1 = cursor.fetchall()
        return render_template('save_new_equipment.html',form_values=form_values, deptid=deptid,venderid=venderid) 
        #print(form_values)
        # return render_template('add_equipment.html',deptid=deptid,venderid=venderid )
    else :
        return ('Please use post method')


@app.route('/parameter_list')
def parameter_list():
    deptid = request.args.get('deptid')
    venderid = request.args.get('venderid')
    equipmentid = request.args.get('equipmentid')
    # for row in data:
    #     equ_parameter_id = row[0]
    #     parameter_name = row[1]  
    #     creation_date = row[2]
    #     remark = row[3]
    #     parameter_list = row[4]
    #     print("para-list",parameter_name)
       

    return render_template('parameter_list.html')


@app.route('/save_reading',methods=['GET', 'POST'])
def save_reading():
    if 'session_id' in session:  
        sessionid = session['session_id']
        if request.method == 'POST' :
            # equipmentid = request.args.get('equipmentid')
            #print(request.form)
            #print(request.form.to_dict())
            form_obj = request.form.to_dict()
            equipmentid = request.form['equipmentid']
            venderid = request.form['venderid']
            deptid = request.form['deptid']
            # form_values = request.form['textall']
            remark = request.form['Remarks']
            approvar_name = request.form['approvar_name']
            approvar_email = request.form['approvar_email']
            try :
               verified1 = request.form['verified']
               varified1 = 0
            except :
                varified1 = 1

            #print ("varified=",verified)
            #if verified != 'on':
            #    verified =0
            #followed = request.form['followed']
            # Get equ_parameter_id from equipmentid
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT equ_name, equ_parameter_id FROM equipment where equ_id =%s',(equipmentid,))        
            data = cursor.fetchall()
            for row in data:
                equ_name = row[0]
                equ_parameter_id = row[1]
        
            # get parameter_names (list) in array defined from equ_parameter_id
            cursor.execute('SELECT parameter_name FROM parameter where equ_parameter_id =%s',(equ_parameter_id,))
            data = cursor.fetchall()
            for row in data:
                parameter_name = row[0]

            para_name = str(parameter_name)
            cursor.execute("SELECT department_name, department_id FROM department where vender_id=%s",(venderid,))
            data = cursor.fetchall()
            #print("venderid im in dept",venderid)
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT name, vender_id, address FROM vender where vender_id=%s',(venderid,))
            data1 = cursor.fetchall()
            timestamp=datetime.now()
            cur_date = timestamp.strftime("%Y-%m-%d")
            # insert all the values along with (coma seperated) data string (parameter_readings in calibrate).
            #cursor.execute('insert  into calibrate (id, equ_id, parameter_readings, perform_date, approvar_name, remark,approvar_email,digitally_signed ) values (%s,%s,%s, %s, %s, %s,%s,%s)', (sessionid,equipmentid,from_values_m,cur_date, approvar_name, remark,approvar_email,verified1,))
            #mysql.connection.commit()
            #print("--------------", form_obj["approvar_name"])
            cursor.execute('insert into calibrate (id, equ_id, parameter_readings, perform_date, approvar_name,approvar_email) values (%s,%s,%s, %s, %s,%s)', (sessionid,equipmentid,form_obj, cur_date,form_obj["approvar_name"],form_obj["approvar_email"]))
            mysql.connection.commit()
            #print ('Parameter=', from_values_m,' Name=',para_list,'Inserted OKLEN=',len(para_list))
            #return "para_name ", parameter_name," Name=",parameter_name
            # return  str(form_values)
            return render_template('/save_reading.html',venderid=venderid ,deptid=deptid)
            # return render_template('previous_reading',approvar_name=approvar_name)
         
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
    #print (obj_ret)
    return obj_ret   

  
@app.route('/json_table', methods = ['GET','POST'])
def jason_table():
    return render_template('json_table.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True) 



