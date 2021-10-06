import pymysql.cursors
from hashlib import sha256
mydb = pymysql.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="b65783d347eaac",
        passwd="7911defd",
        database="heroku_80f10aeef8d10b7"
)
mycursor = mydb.cursor()
#
# mycursor.execute("CREATE TABLE Users (uid INTEGER UNIQUE AUTO_INCREMENT PRIMARY KEY,"
#                  "username VARCHAR(255), "
#                  "firstname VARCHAR(255), "
#                  "lastname VARCHAR(255), "
#                  "pwd VARCHAR(255))")
# mycursor.execute("CREATE TABLE Entries "
#                  "(eid INTEGER PRIMARY KEY UNIQUE AUTO_INCREMENT, uid INTEGER,"
#                 "FOREIGN KEY(uid) REFERENCES "
#                 "Users(uid), normal INTEGER, manic INTEGER, depressed INTEGER,"
#                 "elated INTEGER, down INTEGER, description VARCHAR(255), time DATETIME)")
#mycursor.execute("SHOW TABLES")
# for tb in mycursor:
#     print(tb)
#mycursor.execute("DROP TABLE Entries")
# mycursor.execute("ALTER TABLE Users DROP COLUMN pwd")
# mycursor.execute("ALTER TABLE Users DROP COLUMN gender")
# mycursor.execute("ALTER TABLE Users ADD firstname varchar(255)")
# mycursor.execute("ALTER TABLE Users ADD lastname varchar(255)")
# mycursor.execute("ALTER TABLE USERS ADD uid varchar(255) UNIQUE PRIMARY KEY")
#mycursor.execute("ALTER TABLE Entries ADD elated INTEGER")
#mycursor.execute("ALTER TABLE Entries ADD down INTEGER")
def add_user(firstname, lastname, username, pwd):
    pwd = password_hash(pwd)
    sql = "INSERT INTO USERS (firstname, lastname, username, pwd) VALUES (%s, %s, %s, %s)"
    record = (firstname, lastname, username, pwd)
    mycursor.execute(sql, record)
    mydb.commit()

def login(username, password):
    sql = "SELECT * FROM Users WHERE username = (%s) and pwd= (%s)"
    password = password_hash(password)
    record1 = (username, password)
    mycursor.execute(sql, record1)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return "Login Failed"
    return str(myresult[0])

def get_uid(uname):
    sql = "SELECT uid FROM USERS WHERE `username` = '%s'" % uname
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    result = str(myresult[0])
    result = result.strip("[(\')]',")
    print(result)
    return result

def get_user_info(username):
    sql = "SELECT * FROM USERS WHERE username = ('%s')"
    record = username
    mycursor.execute(sql, record)
    myresult = mycursor.fetchall()
    print(len(myresult))

def password_hash(password):
    h = sha256()
    h.update(password.encode('utf-8'))
    hash = h.hexdigest()
    return hash
def add_entry(username, description, emotions, timedate):
    uid = int(get_uid(username))
    sql = "INSERT INTO ENTRIES (uid, description, time, normal, manic, depressed, elated, down) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    record = (uid, description, timedate, emotions[0], emotions[1], emotions[2], emotions[3], emotions[4])
    mycursor.execute(sql, record)
    mydb.commit()
    sql2 = "SELECT eid FROM ENTRIES ORDER BY eid DESC LIMIT 1;"
    mycursor.execute(sql2)
    result = mycursor.fetchone()
    return str(result).strip("(\',)")
def get_user_entry(username):
    uid = get_uid(username)
    sql = "SELECT eid, normal, manic, depressed, elated, down, description, time FROM ENTRIES WHERE `uid` = '%d' ORDER BY eid DESC LIMIT 10" % int(uid)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    results = []
    for i in range(len(result)):
        results.append(result[i])
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    minimum = min(len(results), 14)
    for i in range(minimum):
        a.append(str(results[i][0]))
    for i in range(minimum):
        b.append(str(results[i][1]))
    for i in range(minimum):
        c.append(str(results[i][2]))
    for i in range(minimum):
        d.append(str(results[i][3]))
    for i in range(minimum):
        e.append(str(results[i][4]))
    for i in range(minimum):
        f.append(str(results[i][5]))
    for i in range(minimum):
        g.append(str(results[i][6]))
    for i in range(minimum):
        h.append(str(results[i][7]))
    return a, b, c, d, e, f, g, h