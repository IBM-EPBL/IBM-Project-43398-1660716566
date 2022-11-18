import getpass
from CURD import connect_db , get_admin_by_username , add_admin
from app import bcrypt

def create_admin():
    connect_db() #connecting to db2
    while(1):
        print("Creating a admin account ")
        admin_id = input("Enter ur new Admin-ID ")
        admin = get_admin_by_username(admin_id)
        if admin:
            print("Admin-Id Already Exist.")
        else:
            break

    for i in range(3):
        paswd = getpass.getpass("Enter password : ")
        cpasswd = getpass.getpass("Confirm password : ")
        if paswd == cpasswd:
            paswd= bcrypt.generate_password_hash(paswd)
            add_admin(admin_id,paswd)
            break
        else:
            print("Password mismatch")


if __name__ == "__main__":
    create_admin()