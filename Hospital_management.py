import mysql.connector as s

con = s.connect(host='localhost', user='root', passwd='root', database='hospital')
cur = con.cursor()


# @_DOCTOR_
# FUNCTION TO ADD, UPDATE, DELETE AND DISPLAY RECORDS
def insertion():
    did = input("Enter Doctor ID:: ")
    name = input("Enter Doctor's Name:: ")
    mobno = int(input('Enter mobno:: '))
    specialisation = input("Enter Doctor's Specialisation:: ")
    fees = int(input("Enter doctor's fee:: "))
    roomno = int(input("Enter Room No.:: "))
    dob = input('Enter the Date of Birth of doctor:: ')
    r = "insert into doctor values(%s,%s,%s,%s,%s,%s,%s)"
    try:
        cur.execute(r, (did, name, mobno, specialisation, fees, roomno, dob))
        con.commit()
        print()
        print("""
====================================
!!!!!!!REGISTERED SUCCESSFULLY!!!!!!
====================================
""")
    except s.Error as err:
        print("Could not register doctor:", err)
        print("(This usually means the Doctor ID already exists.)")


def update():
    did = input("Enter Doctor ID:: ")
    name = input("Enter Doctor's Name:: ")
    mobno = int(input('Enter Contact No.:: '))
    fees = int(input("Enter fee of doctor:: "))
    dob = input('Enter Date of Birth of doctor:: ')
    cur.execute("update doctor set name=%s, mobno=%s, fees=%s, dob=%s where did=%s",
                (name, mobno, fees, dob, did))
    if cur.rowcount == 0:
        print("No doctor found with that ID — nothing was updated.")
    else:
        print("""
====================================
!!!!!!!!!UPDATED SUCCESSFULLY!!!!!!!
====================================
""")
    con.commit()


def deletion():
    did = input('Enter the Doctor ID to delete:: ')
    cur.execute("select did from doctor where did=%s", (did,))
    x = cur.fetchall()
    if x == []:
        print('ID does not exist.')
    else:
        cur.execute("delete from doctor where did=%s", (did,))
        con.commit()
        print("One Doctor record deleted.")


def display():
    cur.execute('select * from doctor')
    print("{:<7}{:<15}{:<15}{:<18}{:<6}{:<7}{}".format(
        "DID", 'NAME', 'CONTACT_NO', 'SPECIALIZATION', 'FEES', 'ROOMNO', 'DOB'))
    print("*" * 80)
    o = cur.fetchall()
    for i in o:
        print("{:<7}{:<15}{:<15}{:<18}{:<6}{:<7}{}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


# @_MEDICAL TEST_
# FUNCTION TO UPDATE AND DISPLAY RECORDS
def addtest():
    roomno = int(input("Enter Room No. :: "))
    test = input("Enter name of test :: ")
    charge = int(input("Enter charge :: "))
    cur.execute("insert into medicaltest values (%s, %s, %s)", (test, roomno, charge))
    con.commit()


def display1():
    cur.execute("select * from medicaltest")
    print("{:<18}{:<5}{:<10}".format("test", "roomno", "charges"))
    p = cur.fetchall()
    for i in p:
        print("{:<18}{:<5}{:<10}".format(i[0], i[1], i[2]))


def update1():
    test = input("Enter name of test :: ")
    charges = int(input("Enter updated charge :: "))
    cur.execute("update medicaltest set charges=%s where test=%s", (charges, test))
    if cur.rowcount == 0:
        print("No test found with that name — nothing was updated.")
    else:
        print("""
====================================
!!!!!!!!!UPDATED SUCCESSFULLY!!!!!!!
====================================
""")
    con.commit()


# @_PATIENT_
# FUNCTION TO ADD, DELETE AND DISPLAY RECORDS
def insert1():
    pid = int(input('Enter Patient ID:: '))
    name = input('Enter Name of Patient:: ')
    age = int(input("Enter Patient's Age:: "))
    gender = input('Enter Gender of Patient:: ')
    address = input('Enter Address of Patient:: ')
    status = input('Status of Patient- (admit/OPD):: ')

    if status.lower() == "admit":
        roomno = input("Enter Room No.:: ")
    elif status.lower() == "opd":
        roomno = "Null"
    else:
        print("Invalid status. Please enter 'admit' or 'OPD'.")
        return

    contact = int(input('Enter Contact No. of Patient:: '))
    did = input("Enter doctor ID:: ")
    t = "insert into patient values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(t, (pid, name, age, gender, address, status, contact, roomno, did))
    print("""
====================================
!!!!!!!REGISTERED SUCCESSFULLY!!!!!!
====================================
""")
    con.commit()


def deletion1():
    pid = input('Enter the Patient ID to delete:: ')
    cur.execute("select pid from patient where pid=%s", (pid,))
    x = cur.fetchall()
    if x == []:
        print('ID does not exist.')
    else:
        cur.execute("delete from patient where pid=%s", (pid,))
        print("""
================================
!!!!!!!DELETED SUCCESSFULLY!!!!!!
================================
""")
        con.commit()


def display2():
    cur.execute("select* from patient")
    print("{:<5}{:<15}{:<5}{:<7}{:<15}{:<10}{:<15}{:<5}".format(
        'pid', 'name', 'age', 'gender', 'address', 'status', 'contact', 'roomno'))
    o = cur.fetchall()
    for i in o:
        print("{:<5}{:<15}{:<5}{:<7}{:<15}{:<10}{:<15}{:<5}".format(
            i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
    con.commit()


# _@_BILL_
# FUNCTION TO GENERATE BILL
def bill():
    billno = int(input("Enter Bill No.:: "))
    pid = int(input("Enter Patient ID:: "))
    cur.execute("select name,did from patient where pid=%s", (pid,))
    data = cur.fetchone()
    if data is None:
        print("No patient found with that ID.")
        return
    patient_name, doctor_id = data

    cur.execute("select name from doctor where did=%s", (doctor_id,))
    o = cur.fetchone()
    if o is None:
        print("The doctor assigned to this patient could not be found.")
        return
    doctor_name = o[0]

    cur.execute("select fees from doctor where did=%s", (doctor_id,))
    o = cur.fetchone()
    doctor_fees = o[0]

    y = input("Enter Test:: ")
    cur.execute("select charges from medicaltest where test=%s", (y,))
    p = cur.fetchone()
    if p is None:
        print("No medical test found with that name.")
        return
    test_charges = p[0]

    z = input("Status(admit or OPD):: ")
    room_charges = 0
    if z.lower() == "admit":
        day1 = 500
        no_of_days = int(input("Enter no. of days:: "))
        room_charges = no_of_days * day1

    total_amount = doctor_fees + test_charges + room_charges
    print("\n\n\n")
    print("************______#BILL#______*****************")
    print("\n\n")
    print(" PATIENT NAME: ", patient_name)
    print(" DOCTOR NAME: ", doctor_name)
    print(" DOCTOR CHARGES: ", doctor_fees)
    print(" TEST NAME: ", y)
    print(" TEST CHARGES: ", test_charges)
    print(" ROOM CHARGES: ", room_charges)
    print(" TOTAL AMOUNT: ", total_amount)
    print("SERVICE CHARGE : ", total_amount * .15)
    print("-" * 60)
    print("NET AMOUNT PAYABLE:", total_amount + total_amount * .15)
    print("\n\n")
    print(" ---------------THANK YOU---------------------- ")
    print("PLEASE GIVE US A CHANCE TO SERVE AGAIN")


# --------------MAIN PROGRAM---------------
print('-------------------------------------------------------------------------')
print('*************************************************')
print()
print('__WELCOME TO HOSPITAL MANGEMENT__')
print()
print('*****************************************')
print('\n')

while True:
    print("*****MAIN MENU*******")
    print("1. Doctor's Menu ")
    print("2. Patient's Menu ")
    print("3. Medical Tests")
    print("4. Billing ")
    print("5. Exit")
    x = int(input("enter your choice : "))
    if x == 1:
        print(' a.Add Records OF Doctor')
        print(' b.Update The Records of Doctor')
        print(' c.Delete The Records of Doctor')
        print(' d.Display the Records of Doctor')
        a = input("Enter your choice:: ")
        if a == 'a':
            print("Add records of Doctor")
            insertion()
        elif a == 'b':
            print("update record of Doctor")
            update()
        elif a == 'c':
            print("Delete record of doctor")
            deletion()
        elif a == 'd':
            print("display the record of Doctor")
            display()
    elif x == 2:
        print(' a.Add Records of Patient')
        print(' b.Delete The Records of Patient')
        print(' c.Display the Records of Patient')
        a = input("Enter your choice:: ")
        if a == 'a':
            print('**Add Records of Patient**')
            insert1()
        elif a == 'b':
            print('**Delete Records of patient**')
            deletion1()
        elif a == 'c':
            print('**Display Records of Patient**')
            display2()
    elif x == 3:
        print(' a.Add medical test')
        print(' b.Update records of medical test')
        print(' c.Display records of medical test')
        a = input("Enter your choice:: ")
        if a == 'a':
            while True:
                addtest()
                ch = input("Press y to add more tests ")
                if ch != 'y':
                    break
        elif a == 'b':
            print('**Update medical test records**')
            update1()
        elif a == 'c':
            print('**Display records of medical test**')
            display1()
    elif x == 4:
        print('**Total Amount**')
        bill()
    elif x == 5:
        break
    else:
        print("Invalid Choice. Please enter again.")
