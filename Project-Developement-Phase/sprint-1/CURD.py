from ctypes import addressof
from sqlite3 import adapt
from flask_login import UserMixin
import ibm_db


# def connect_to_db():
db2=''

class Dict2Class(UserMixin):

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key.lower(), my_dict[key])


def connect_db():
    """
        This function used to connect the db2 database and
        store the db instance in db2.
    """
    global db2
    hostname = "824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
    uid = "gdr94333"
    pwd= "PVpwec4jesVc8H3N"
    driver = "{IBM DB2 ODBC DRIVER}"
    db="bludb"
    port = "30119"
    # protocol = "TCPIP"
    cert = "certificate.arm"

    dsn = (

        "DATABASE={0};"
        "HOSTNAME={1};"
        "PORT={2};"
        "UID={3};"
        "SECURITY=SSL;"
        "SSLServerCertificate={4};"
        "PWD={5};".format(db,hostname,port,uid,cert,pwd)
    )

    print(dsn)
    try:
        db2= ibm_db.connect(dsn,"","")
    except:
        print("unable to connect",ibm_db.conn_errormsg())

        return -1
    return 1


def add_user(username,password,first_name,last_name,age,phone,weight,blood_group):
    """
        Add user to the db2.
    """
    insert = "insert into user (username,password,firstname,lastname,age,phone,weight,bloodgroup) values (?,?,?,?,?,?,?,?);"
    params = (username,password,first_name,last_name,age,phone,weight,blood_group)

    stmt_insert = ibm_db.prepare(db2,insert)

    try:
        ibm_db.execute(stmt_insert,params)

    except Exception as e:
        print(e)


def get_user_by_id(id):
    """
        Fetch the  user instance by id form db2 and return user
        instance.

    """
    find = "SELECT * FROM user WHERE id = {}".format(id)
    stmt_select = ibm_db.exec_immediate(db2,find)
    # ibm_db.bind_param(db2,1,stmt_find)
    try:
        # ibm_db.execute(stmt_find)
        cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print(e)
        return -1
    return Dict2Class(cols) if cols else False


def get_user_by_username(username):
    """
        Fetch the  user instance by username form db2 and return user
        instance.

    """
    find = "SELECT * FROM user WHERE username = '{}'".format(username)
    stmt_select = ibm_db.exec_immediate(db2,find)
    # ibm_db.bind_param(db2,1,stmt_find)
    try:
        # ibm_db.execute(stmt_find)
        cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print(e)
        return -1

    return Dict2Class(cols) if cols else False




def get_admin_by_username(username):
    find = "SELECT * FROM ADMIN WHERE adminid = '{}'".format(username)
    stmt_select = ibm_db.exec_immediate(db2,find)
    # ibm_db.bind_param(db2,1,stmt_find)
    try:
        # ibm_db.execute(stmt_find)
        cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print(e)
        return -1

    return Dict2Class(cols) if cols else False


def add_admin(username,password):
    hospital = input("Enter Hospital :")
    address = input("Enter Address : ")
    add = "INSERT INTO admin(adminid , password , hospital , address) values(?,?,?,?)"
    params = (username,password,hospital,address)

    stmt_insert = ibm_db.prepare(db2,add)

    try:
        ibm_db.execute(stmt_insert,params)

    except Exception as e:
        print(e)


def get_admin_by_id(id):
    find = "SELECT * FROM admin WHERE id = {}".format(id)
    stmt_select = ibm_db.exec_immediate(db2,find)
    # ibm_db.bind_param(db2,1,stmt_find)
    try:
        # ibm_db.execute(stmt_find)
        cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print(e)
        return -1
    return Dict2Class(cols) if cols else False



# if __name__ =="__main__":
    # connect_to_db()