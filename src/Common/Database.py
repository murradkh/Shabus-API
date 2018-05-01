from flask import Flask, current_app
from flask_security import Security
from flask_security.utils import verify_password
import bcrypt

t = (bcrypt.hashpw('murrad'.encode(),bcrypt.gensalt()))
print(t)
print(bcrypt.checkpw('murrad123'.encode(), "$2b$12$Wq6AG.9ubHOk81VVZrLkYuuzBrGzav9XU5m0K458Yg2Zxb/t5.53.".encode()))


# with app.app_context():
#     verify_password('Murrad123', '$2b$12$Wq6AG.9ubHOk81VVZrLkYuuzBrGzav9XU5m0K458Yg2Zxb/t5.53.')















import psycopg2 as p


try:
    connection = p.connect("dbname='d2ink2ug7q191f' user='ewvctvrtnsgwwc' host='ec2-54-228-251-254.eu-west-1.compute.amazonaws.com' password='35b1b3c3129277497c85646ebd99cdf2edecc490cd03b4cb0532656d7fbfd962' port='5432'")
    connection.autocommit = True
    cursor = connection.cursor()
except:
    print("Cannot connect to database")

cursor = connection.cursor()
create_table_command = 'select * from user_'
cursor.execute(create_table_command)
data = cursor.fetchall()
print(data)
#
