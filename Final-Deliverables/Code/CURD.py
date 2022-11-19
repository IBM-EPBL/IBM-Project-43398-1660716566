from threading import Thread
from flask_login import UserMixin
import ibm_db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# def connect_to_db():
db2=''
SENDGRID = "SG.vwdM4_lZTc6mD0FrOqVgrA.gm4cNNKsEovlfiUP_BLrer1A2twS5YGZMxnLgR_rF8kajk"

class Dict2Class(UserMixin):

    def __init__(self, my_dict):
        for key in my_dict:

            if type(my_dict[key]) == type(" "):
                setattr(self, key.lower(), my_dict[key].strip())
                continue

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


def send_mail(message):
    try:
        sg = SendGridAPIClient(SENDGRID)
        response = sg.send(message)
        return 1
    except Exception as E:
        print(E)
        return -1

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


def get_admin_by_list(li=None):
    if li:
        li = list(map(str,set(li)))
        select = "SELECT * FROM admin where({})".format("".join(li))
    else:
        select = "SELECT * FROM admin;"

    stmt_select = ibm_db.exec_immediate(db2,select)
    try:
        cols = ibm_db.fetch_assoc(stmt_select)
        d = {}
        while cols:
            obj=Dict2Class(cols)
            d[obj.id] = obj
            cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print (e)
        return -1
    return d


def get_user_by_list(li=None):
    if li:
        li = list(map(str,set(li)))
        select = "SELECT * FROM user where({})".format("".join(li))
    else:
        select = "SELECT * FROM user;"

    stmt_select = ibm_db.exec_immediate(db2,select)
    try:
        cols = ibm_db.fetch_assoc(stmt_select)
        d = {}
        while cols:
            obj=Dict2Class(cols)
            d[obj.id] = obj
            cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print (e)
        return -1
    return d

def get_plasma_by_id(id):
    find = "SELECT * FROM plasma WHERE id = {}".format(id)
    stmt_select = ibm_db.exec_immediate(db2,find)
    # ibm_db.bind_param(db2,1,stmt_find)
    try:
        # ibm_db.execute(stmt_find)
        cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print(e)
        return -1
    return Dict2Class(cols) if cols else False


def get_all_request():
    select = "SELECT * FROM plasma;"
    stmt_select = ibm_db.exec_immediate(db2,select)
    try:
        cols = ibm_db.fetch_assoc(stmt_select)
        d = {}
        while cols:
            obj=Dict2Class(cols)
            d[obj.id] = obj
            cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print (e)
        return -1

    l =[ i.recipientid for i in d.values()]
    ad = get_admin_by_list(l)
    for i in d.values():
        i.recipientid = ad[i.recipientid]
    return d


def send_mail_req_update(id,user_id):
    user = get_user_by_id(user_id)
    plasma = get_all_request()[id]

    message = Mail(
        from_email="pradeep.s.ece.2019@snsct.org",
        to_emails=user.username,
    )

    message.dynamic_template_data = {
        "id":plasma.id,
        "d_name" : user.firstname,
        "hospital" : plasma.recipientid.hospital,
        "blood" :plasma.bloodgroup,
        "location" : plasma.recipientid.address,
        "units":plasma.units
    }
    message.template_id = "d-39ef32996348468d827e32927984e907"
    ret = send_mail(message)
    return ret


def request_update(id,user_id):
    update = "update plasma set donorid = {} where id = {}".format(user_id,id)
    update_stmt = ibm_db.prepare(db2,update)
    t = Thread(target=send_mail_req_update,args=(id,user_id))
    t.start()
    try:
        ibm_db.execute(update_stmt)

    except Exception as E:
        print(E)
        return -1
    return 1

def send_mail_req_undo(id,user_id):
    user = get_user_by_id(user_id)
    plasma = get_all_request()[id]

    message = Mail(
        from_email="pradeep.s.ece.2019@snsct.org",
        to_emails=user.username,
    )

    message.dynamic_template_data = {
        "id":plasma.id,
        "d_name" : user.firstname,
        "hospital" : plasma.recipientid.hospital,
        "blood" :plasma.bloodgroup,
        "location" : plasma.recipientid.address,
        "units":plasma.units
    }
    message.template_id = "d-9a511dd0641445dcb55096eabf526be8"
    ret = send_mail(message)
    return ret


def undo_request_update(id,userid):
    update = "update plasma set donorid = NULL where id = {}".format(id)
    update_stmt = ibm_db.prepare(db2,update)
    th = Thread(target=send_mail_req_undo,args=(id,userid))
    th.start()
    try:
        ibm_db.execute(update_stmt)
    except Exception as E:
        print(E)
        return -1
    return 1



def get_all_users():
    select = "SELECT * FROM user;"
    stmt_select = ibm_db.exec_immediate(db2,select)
    try:
        cols = ibm_db.fetch_assoc(stmt_select)
        d = {}
        while cols:
            obj=Dict2Class(cols)
            d[obj.id] = obj
            cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print (e)
        return -1

    return d.values()


def get_all_pending_request(id):
    select = "SELECT * FROM plasma where donorid is not NULL and recipientid = {};".format(id)
    stmt_select = ibm_db.exec_immediate(db2,select)
    try:
        cols = ibm_db.fetch_assoc(stmt_select)
        d = {}
        while cols:
            obj=Dict2Class(cols)
            d[obj.id] = obj
            cols = ibm_db.fetch_assoc(stmt_select)
    except Exception as e:
        print (e)
        return -1

    l =[ i.donorid for i in d.values()]
    ad = get_user_by_list(l)
    for i in d.values():
        i.donorid = ad[i.donorid]

    return d.values()

def update_pending_plasma_mail(id):

    plasma = get_plasma_by_id(id)
    user = get_user_by_id(plasma.donorid)
    admin = get_admin_by_id(plasma.recipientid)
    message = Mail(
        from_email="pradeep.s.ece.2019@snsct.org",
        to_emails=user.username,
    )
    message.dynamic_template_data = {
        "id":plasma.id,
        "d_name" : user.firstname,
        "hospital" : admin.hospital,
        "blood" :plasma.bloodgroup,
        "location" : admin.address,
        "units":plasma.units
    }
    message.template_id = "d-2f7eb31f6b0948f9a3f8f1ba0741cff9"
    ret = send_mail(message)
    return ret


def update_pending_plasma(id):
    update = "update plasma set isactive = false where id = {}".format(id)
    update_stmt = ibm_db.prepare(db2,update)
    th = Thread(target=update_pending_plasma_mail,args=(id,))
    th.start()
    try:
        ibm_db.execute(update_stmt)
    except Exception as E:
        print(E)
        return -1
    return 1


def create_plasma_request(unit,blood,user):
    insert = "insert into plasma (bloodgroup,units,recipientid,isactive) values (?,?,?,?);"
    params = (blood,unit,user.id,"true")

    stmt_insert = ibm_db.prepare(db2,insert)

    try:
        ibm_db.execute(stmt_insert,params)

    except Exception as e:
        print(e)



# if __name__ =="__main__":
#     connect_db()
#     print(get_all_request())