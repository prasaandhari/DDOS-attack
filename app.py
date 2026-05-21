from flask import Flask, render_template, flash, request,session,send_file,redirect
import mysql.connector
from werkzeug.utils import secure_filename
import os
from green_security import check_attempts, reset_attempts, send_alert, get_energy_mode
import socket
import datetime
import joblib
import time
import yagmail

# Load ML model

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
model = joblib.load("attack_model.pkl")
import yagmail
@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/adminlogin")
def AdminLogin():
    return render_template('admin.html')
@app.route("/userfile")
def userfile():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM file ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)
    return render_template('userfile.html',data=data)
@app.route("/viewattack")
def viewattack():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM attacker1")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)
    return render_template('viewattack.html',data=data)
@app.route("/NewUser")
def NewUser():
    return render_template('register.html')
@app.route("/UserLogin")
def UserLogin():
    return render_template('stud.html')
@app.route("/AdminHome")
def AdminHome():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM regtb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)
    return render_template('AdminHome.html', data=data)

@app.route("/adminuserdetails")
def adminuserdetails():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM userregtb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)
    return render_template('adminuserdetails.html', data=data)

@app.route("/newidcreat")
def newidcreat():
    conn = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='1cloud'
    )
    cur = conn.cursor()

    # 🔹 USER DATA
    cur.execute("SELECT * FROM userregtb")
    users = cur.fetchall()

    # 🔹 OWNER DATA (if same table, reuse OR change table name if different)
    cur.execute("SELECT * FROM regtb")
    owners = cur.fetchall()

    # 🔹 FETCH CREATED USER IDS
    cur.execute("SELECT userid FROM userid")
    user_ids = cur.fetchall()
    created_user_ids = [i[0] for i in user_ids]

    # 🔹 FETCH CREATED OWNER IDS
    cur.execute("SELECT userid FROM ownerid")
    owner_ids = cur.fetchall()
    created_owner_ids = [i[0] for i in owner_ids]

    conn.close()

    return render_template(
        "newidcreat.html",
        data=users,
        data1=owners,
        created_user_ids=created_user_ids,
        created_owner_ids=created_owner_ids
    )




@app.route("/rNewUser", methods=['GET', 'POST'])
def rNewUser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['phone']
        uname = request.form['uname']
        password = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
    return render_template('stud.html')
@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            data1 = 'Username or Password is wrong'

            return render_template('goback.html', data=data1)
        else:
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb where UserName='"+ session['uname'] +"' ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)
            return render_template('UserHome.html',data=data)
@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute("SELECT * from admintb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)
        else:
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb  ")
            data = cur1.fetchall()
            # return 'file register successfully'
            #return render_template('order.html', data=data)
            return render_template('AdminHome.html',data=data)
@app.route("/userhome")
def UserHome():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where  UserName= '" + uname + "' ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)
@app.route("/fileupload")
def fileupload():
    return render_template('Fileupload.html')
@app.route("/upload1", methods=['GET', 'POST'])
def upload1():
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        uname = session['uname']
        f = request.files['file']
        f.save(secure_filename(f.filename))
        file_path=secure_filename(f.filename)
        size=os.path.getsize(file_path)
        from tinyec import registry
        import secrets
        curve = registry.get_curve('brainpoolP256r1')
        def compress_point(point):
            return hex(point.x) + hex(point.y % 2)[2:]
        def ecc_calc_encryption_keys(pubKey):
            ciphertextPrivKey = secrets.randbelow(curve.field.n)
            ciphertextPubKey = ciphertextPrivKey * curve.g
            sharedECCKey = pubKey * ciphertextPrivKey
            return (sharedECCKey, ciphertextPubKey)
        def ecc_calc_decryption_key(privKey, ciphertextPubKey):
            sharedECCKey = ciphertextPubKey * privKey
            return sharedECCKey
        privKey = secrets.randbelow(curve.field.n)
        pubKey = privKey * curve.g
        print("private key:", hex(privKey))
        print("public key:", compress_point(pubKey))
        (encryptKey, ciphertextPubKey) = ecc_calc_encryption_keys(pubKey)
        print("ciphertext pubKey:", compress_point(ciphertextPubKey))
        print("encryption key:", compress_point(encryptKey))
        decryptKey = ecc_calc_decryption_key(privKey, ciphertextPubKey)
        print("decryption key:", compress_point(decryptKey))
        import string
        import random
        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        key1=id_generator()
        def id_generator1(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        key2 = id_generator1()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO file VALUES ('','" + name + "','" + details + "','" + uname + "','" + f.filename + "','" + str(size) + "','" + str(key1) + "','" + str(key2) + "')")
        conn.commit()
        conn.close()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cur = conn.cursor()
        cur.execute("select * from regtb where UserName='" + uname + "'")
        data = cur.fetchone()
        email = data[4]

        mail = 'testsam360@gmail.com';
        password = 'rddwmbynfcbgpywf';
        # list of email_id to send the mail
        li = [email]
        body = "Key---" + key2

        yag = yagmail.SMTP(mail, password)

        for dest in li:
            yag.send(
                to=dest,
                subject="File Download Key...!",
                contents=body,

            )
        print("Mail sent to all...!")
        return 'file register successfully'
@app.route("/viewfile")
def viewfile():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur = conn.cursor()
    cur.execute("SELECT * FROM file where  username= '" + uname + "' ")
    data = cur.fetchall()
    return render_template('viewfile.html',data=data)
@app.route("/dwonload")
def dwonload():
    pid = request.args.get('pid')
    uname = session['uname']
    path=pid
    return send_file(path, as_attachment=True)

@app.route("/dwonload1")
def dwonload1():
    pid = request.args.get('pid')
    session['fid']=pid
    uname = session['uname']
    path=pid
    return render_template('key.html')
@app.route("/fkey", methods=['GET', 'POST'])
def fkey():

    if request.method == 'POST':

        start = time.time()

        filekey = request.form['filekey']
        fid = session['fid']
        uname = session['uname']

        conn = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='1cloud'
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM file WHERE id=%s AND prkey=%s",(fid,filekey))
        data = cursor.fetchone()

        if data is None:

            # Wrong key attempt counter
            session['attempt'] = session.get('attempt',0) + 1
            attempts = session['attempt']

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)

            now = datetime.datetime.now()

            # Energy usage
            end = time.time()
            power = 65
            energy = power * (end - start)

            # ML features
            time_gap = 2
            ip_change = 0

            prediction = model.predict([[attempts,time_gap,ip_change,energy]])

            status = "Normal User"
            if prediction[0] == 1:
                status = "⚠ Attacker Detected"

            # save attacker log
            cursor.execute(
                "INSERT INTO attacker1(name,ipaddress,date) VALUES(%s,%s,%s)",
                (hostname,ip_address,now)
            )

            conn.commit()

            # Send email alert
            try:
                yag = yagmail.SMTP("testsam360@gmail.com","rddwmbynfcbgpywf")

                subject = "Green Cybersecurity Alert"

                body = f"""
                Alert Notification

                User : {uname}
                Hostname : {hostname}
                IP Address : {ip_address}

                Wrong Attempts : {attempts}

                Energy Used : {energy:.2f} Joules

                AI Prediction : "Attacker Detected"
                Time : {now}

                Secure Cloud Storage Monitoring System
                """
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
                cur = conn.cursor()
                cur.execute("select * from regtb where UserName='" + uname + "'")
                data = cur.fetchone()
                email = data[4]

                yag.send(email,subject,body)

            except:
                print("Mail sending failed")

            conn.close()

            return "<h3 style='color:red'>Invalid File Key</h3>"

        else:

            path = data[4]

            end = time.time()
            power = 65
            energy = power * (end - start)

            now = datetime.datetime.now()

            # Send energy report mail
            try:

                yag = yagmail.SMTP("yourgmail@gmail.com","your_app_password")

                subject = "Energy Usage Report"

                body = f"""
                File Download Energy Report

                User : {uname}

                File Path : {path}

                

                Time : {now}
                """
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
                cur = conn.cursor()
                cur.execute("select * from regtb where UserName='" + uname + "'")
                data = cur.fetchone()
                email = data[4]

                yag.send(email,subject,body)

            except:
                print("Mail failed")

            conn.close()

            return send_file(path, as_attachment=True)
@app.route("/userrequest")
def userrequest():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfilerequest where  oname= '" + uname + "' and  status='Waiting'")
    data = cur.fetchall()
    return render_template('userquest.html',data=data)
@app.route("/Datauser")
def Datauser():

    return render_template('datauserlogin.html')
@app.route("/datauserregister")
def datauserregister():

    return render_template('datauserregister.html')

@app.route("/datauserlogin", methods=['GET', 'POST'])
def datauserlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['duname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute("SELECT * from userregtb where UserName='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            data1 = 'Username or Password is wrong'

            return render_template('goback.html', data=data1)
        else:
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM userregtb where UserName='"+ session['duname'] +"' ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)
            return render_template('DataUserHome.html',data=data)

@app.route("/rNewDataUser", methods=['GET', 'POST'])
def rNewDataUser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['phone']
        uname = request.form['uname']
        password = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO userregtb VALUES ('','" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
    return render_template('datauserlogin.html')

@app.route("/datauserhome")
def datauserhome():

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM userregtb where UserName='"+ session['duname'] +"' ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)
            return render_template('DataUserHome.html',data=data)


@app.route("/datauserfile")
def datauserfile():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM file ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)
    return render_template('DataUserFile.html', data=data)

@app.route("/Requestfile", methods=["POST"])
def Requestfile():
    pid = request.form.get('pid')
    unique_id = request.form.get('unique_id')
    uname = session['duname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur = conn.cursor()

    # 🔹 user email
    cur.execute("SELECT * FROM userregtb WHERE UserName=%s", (uname,))
    user_data = cur.fetchone()
    email = user_data[4]

    # 🔹 file details
    cur.execute("SELECT * FROM file WHERE id=%s", (pid,))
    file_data = cur.fetchone()

    fname = file_data[1]
    details = file_data[2]
    oname = file_data[3]
    filename = file_data[4]
    prkey = file_data[7]


    cur.execute("""
        INSERT INTO userfilerequest
        (fid, fname, details, oname, filename, prkey, uname, email, unique_id, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Waiting')
    """, (pid, fname, details, oname, filename, prkey, uname, email, unique_id))

    conn.commit()
    conn.close()

    return "✅ Request Sent Successfully"

@app.route("/datauserviewfile")
def datauserviewfile():
    uname=session['duname']
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM userfilerequest where uname='"+uname+"' ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)
    return render_template('datauserviewfile.html', data=data)

@app.route("/userdwonload1")
def userdwonload1():
    pid = request.args.get('pid')
    session['ffid']=pid
    uname = session['duname']
    path=pid
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM userfilerequest where uname='" + uname + "' and id='"+pid+"' and status='Accepted' ")
    data = cur1.fetchone()
    if data is None:
        return "File Not Dwonlaod"
    else:
        return render_template('key1.html')



@app.route("/fkey1", methods=['GET', 'POST'])
def fkey1():
    error = None
    if request.method == 'POST':
        filekey = request.form['filekey']
        print(filekey)
        fid = session['ffid']
        print(fid)
        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute("SELECT * from userfilerequest where id='" + str(fid) + "' and prkey='" + str(filekey) + "'")
        data = cursor.fetchone()
        if data is None:
            import socket
            h_name = socket.gethostname()
            IP_addres = socket.gethostbyname(h_name)
            print("Host Name is:" + h_name)
            print("Computer IP Address is:" + IP_addres)
            import datetime
            date = datetime.datetime.now()
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO attacker1 VALUES ('','" + h_name + "','" + IP_addres + "','" + str(date) + "')")
            conn.commit()
            conn.close()
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cursor1 = conn1.cursor()
            cursor1.execute("SELECT * from userfilerequest where id='" + str(fid) + "'")
            data1 = cursor1.fetchone()
            oname=data1[4]

            conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
            cursor11 = conn11.cursor()
            cursor11.execute("SELECT * from regtb where UserName='" + str(oname) + "'")
            data11 = cursor11.fetchone()
            email=data11[4]
            mail = 'testsam360@gmail.com';
            password = 'rddwmbynfcbgpywf';
            # list of email_id to send the mail
            li = [email]
            body = ""

            yag = yagmail.SMTP(mail, password)

            for dest in li:
                yag.send(
                    to=dest,
                    subject="Unkown User Try to Access Your File...!",
                    contents=body,

                )
            print("Mail sent to all...!")



            return "Key invaild"
        else:
            path = data[5]
            return send_file(path, as_attachment=True)


@app.route("/checkfile")
def checkfile():
    fname = request.args.get('id')
    str(fname)



    import os
    import time

    # Specify the file path
    file_path = fname

    # Check if the file exists
    if os.path.exists(file_path):
        # Get the last modified time of the file
        last_modified_time = os.path.getmtime(file_path)

        # Get the current time
        current_time = time.time()

        # Define a threshold (e.g., 60 seconds or 1 minute)
        threshold = 60  # in seconds

        # Check if the file was modified within the last threshold period
        if current_time - last_modified_time < threshold:
            p="The file '"+str(file_path)+"' has been modified in the last '"+str(threshold)+"' seconds."
            print(f"The file {file_path} has been modified in the last {threshold} seconds.")
        else:
            p="The file '"+str(file_path)+"' has NOT been modified in the last '"+str(threshold)+"' seconds."
            print(f"The file {file_path} has NOT been modified in the last {threshold} seconds.")
    else:
        p="The file '"+str(file_path)+"' does not exist."
        print(f"The file {file_path} does not exist.")

    return p

import yagmail

@app.route("/create_unique_id")
def create_unique_id():
    uid = request.args.get("uid")

    conn = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='1cloud'
    )
    cur = conn.cursor()

    # get user details
    cur.execute("SELECT * FROM userregtb WHERE id=%s", (uid,))
    user = cur.fetchone()

    name = user[1]
    email = user[4]

    # check already created
    cur.execute("SELECT * FROM userid WHERE userid=%s", (uid,))
    if cur.fetchone():
        return "ID already created"

    # generate unique id
    import random, string
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # insert
    cur.execute("INSERT INTO userid (userid, unique_id) VALUES (%s,%s)", (uid, unique_id))
    conn.commit()

    # -------- SEND MAIL --------
    try:
        yag = yagmail.SMTP("testsam360@gmail.com", "rddwmbynfcbgpywf")

        subject = "Your Unique ID - Secure Cloud"

        body = f"""
Hello {name},

Your User Unique ID has been created successfully.

🔐 Unique ID: {unique_id}

Use this ID for secure access.

Thank you,
Secure Cloud Team
"""

        yag.send(to=email, subject=subject, contents=body)

    except Exception as e:
        print("Mail Error:", e)

    # ---------------------------

    return redirect("/newidcreat")
@app.route("/ownercreate_unique_id")
def ownercreate_unique_id():
    uid = request.args.get("uid")

    conn = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='1cloud'
    )
    cur = conn.cursor()

    # get owner details
    cur.execute("SELECT * FROM regtb WHERE id=%s", (uid,))
    owner = cur.fetchone()

    name = owner[1]
    email = owner[4]

    # check already created
    cur.execute("SELECT * FROM ownerid WHERE userid=%s", (uid,))
    if cur.fetchone():
        return "Owner ID already created"

    # generate unique id
    import random, string
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # insert
    cur.execute("INSERT INTO ownerid (userid, unique_id) VALUES (%s,%s)", (uid, unique_id))
    conn.commit()

    # -------- SEND MAIL --------
    try:
        yag = yagmail.SMTP("testsam360@gmail.com", "rddwmbynfcbgpywf")

        subject = "Your Owner Unique ID - Secure Cloud"

        body = f"""
Hello {name},

Your Owner Unique ID has been created successfully.

🔐 Unique ID: {unique_id}

Use this ID for secure cloud access.

Thank you,
Secure Cloud Team
"""

        yag.send(to=email, subject=subject, contents=body)

    except Exception as e:
        print("Mail Error:", e)

    # ---------------------------

    return redirect("/newidcreat")


@app.route("/accept")
def accept():
    pid = request.args.get('pid')


    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM userfilerequest where id='"+pid+"'")
    data = cur1.fetchone()
    if data is None:
        return "File Not Dwonlaod"
    else:

        email=data[8]
        uqid=data[9]
        pkey=data[6]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute(
            "update userfilerequest set status='Accepted' where id='"+pid+"'")
        conn.commit()
        conn.close()
        mail = 'testsam360@gmail.com';
        password = 'rddwmbynfcbgpywf';
        # list of email_id to send the mail
        li = [email]
        body = "Key---" + pkey

        yag = yagmail.SMTP(mail, password)

        for dest in li:
            yag.send(
                to=dest,
                subject="File Download Key...!",
                contents=body,

            )
        print("Mail sent to all...!")
        return 'User Request Accepted successfully'


        return render_template('key1.html')


@app.route("/reject")
def reject():
    pid = request.args.get('pid')


    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM userfilerequest where id='"+pid+"'")
    data = cur1.fetchone()
    if data is None:
        return "File Not Dwonlaod"
    else:
        email=data[8]
        uname=data[7]
        pkey=data[6]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
        cursor = conn.cursor()
        cursor.execute(
            "update userfilerequest set status='reject' where id='"+pid+"'")
        conn.commit()
        conn.close()


        mail = 'testsam360@gmail.com';
        password = 'rddwmbynfcbgpywf';
        # list of email_id to send the mail
        li = [email]
        body = "Notification"
        yag = yagmail.SMTP(mail, password)
        for dest in li:
            yag.send(
                to=dest,
                subject="File Owner Reject for your File Access Request...!",
                contents=body,

            )
        print("Mail sent to all...!")
        return 'User Request rejected successfully'

        return render_template('key1.html')




@app.route("/check_unique")
def check_unique():
    pid = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1cloud')
    cur = conn.cursor()

    # 🔹 get request unique id
    cur.execute("SELECT unique_id FROM userfilerequest WHERE id=%s", (pid,))
    req = cur.fetchone()

    if not req:
        return {"status": "invalid"}

    unique_id = req[0]

    # 🔹 check in userid table
    cur.execute("SELECT * FROM userid WHERE unique_id=%s", (unique_id,))
    valid = cur.fetchone()

    conn.close()

    if valid:
        return {"status": "valid"}
    else:
        return {"status": "invalid"}





def main():
    app.run(debug=True, use_reloader=True)
if __name__ == '__main__':
    main()