#!/usr/bin/env python3

import mysql.connector
import os

### Creed for db connect
config = {
  'user': '',
  'password': '',
  'host': 'localhost',
  'database': 'asterisk',
  'raise_on_warnings': True
}

## DB Coloums
# sip_id
# depName
# Sip_Pass
# Sip_Number
# Sip_Mailbox

### Class will contain Sip users, methods will be there creedentials
## Name is mandatory to init objects, other methods have default value - 0
class Sip_Acc(object):
    """This is a class of sip users"""

    def __init__(self, Name, Passw=0, Dep=0, Number=0, Mailbox=0):
        """Method stored creedentials"""
        self.Name = Name
        self.Passw = Passw
        self.Dep = Dep
        self.Number = Number
        self.Mailbox = Mailbox

### Function - conect to db and ask query
### return data from sql query
def sql_query(query):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    datas = []
    for data in cursor:
        data = str(data)
        # Delete garbig from data
        data1 = data.replace(r"('", "")
        data2 = data1.replace(r"',)", "")
        data1 = data2.replace(r"(", "")
        data2 = data1.replace(r",)", "")
    #print(data2)
    return(data2)
    cursor.close()
    cnx.close()

### Query to select all users from table OUTGOIN of Asterisk DB
query_users = ("SELECT sip_id FROM OUTGOING WHERE 1")

## 1st sql query
## Open conection to DB
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)
cursor.execute(query_users)

## Init list
sip_users = []

# Filing the list sip_users
for sip_user in cursor:
    sip_user = str(sip_user)
    user1 = sip_user.replace(r"('", "")
    user2 = user1.replace(r"',)", "")
    sip_users.append(user2)
# closing connection to DB
cursor.close()
cnx.close()

## List with all users from table
#print(sip_users)

### Init objects sip users, throw there names
### Dictionary - each key refer to object
dict = {user: Sip_Acc(Name=user) for user in sip_users}
# dict[username].method

### SQLs query
query_Dep = ("SELECT DepName FROM OUTGOING WHERE sip_id LIKE '{}'")
query_Pass = ("SELECT Sip_Pass  FROM OUTGOING WHERE sip_id LIKE '{}'")
query_Number = ("SELECT Sip_Number FROM OUTGOING WHERE sip_id LIKE '{}'")
query_Mailbox = ("SELECT Sip_Mailbox FROM OUTGOING WHERE sip_id LIKE '{}'")

### Init objects in circle, each method is data from table
for user in dict:
    # Ask sql for data
    dep = sql_query(query_Dep.format(user))
    passw = sql_query(query_Pass.format(user))
    number = sql_query(query_Number.format(user))
    mailbox = sql_query(query_Mailbox.format(user))
    # Init objects
    dict[user] = Sip_Acc(Name=user, Dep=dep, Passw=passw, Number=number, Mailbox=mailbox)
    print("------------------------")
    print(dict[user].Name)
    print(dict[user].Dep)
    print(dict[user].Passw)
    print(dict[user].Number)
    print(dict[user].Mailbox)
    print("------------------------")


### List whith Deps names
users_deps = []
for user in dict:
    users_deps.append(dict[user].Dep)
#print(users_deps)

# Unic value of dep name
users_deps_u = []
for dep in users_deps:
    if dep not in users_deps_u:
        users_deps_u.append(dep)
#print(users_deps_u)


### Blank for conf files
#-------------sip.conf-----------------------
mysipconf1 = "[{}](internal-phone,my-codecs)"
mysipconf2 = "        secret = {}"
mysipconf3 = "        mailbox = {}"

#-------------localusers.conf----------------
mylocalus1 = "exten => {1},1,Goto({0},1)"
mylocalus2 = "exten => {0},hint,SIP/{0}"
mylocalus3 = "exten => {0},1,Dial(SIP/{0},,tk)"
mylocalus4 = "       same => n,Hangup()"

# Separator, for deps
separ = ";---------------------{}-Dep-------------------------"


## Forming conf files for asterisk
# Open conf files to write
sipconf = open('/etc/asterisk/my-sip.conf', 'w')
usersconf = open('/etc/asterisk/my-localusers.conf', 'w')

mylocalus0 = "[LocalUsers]"
usersconf.write(mylocalus0 + '\n')

## Fanction is writing conf files
def Wr_conf(dep_n):
    # Separ for my-sip.conf
    sipconf.write(separ.format(dep_n) + '\n')
    sipconf.write('\n')
    # Separ for my-localusers.conf
    usersconf.write(separ.format(dep_n) + '\n')
    usersconf.write('\n')
    for user in dict:
        if dict[user].Dep == dep_n:
            ## Creat users only whith password
            if dict[user].Passw != "":
                ## my-sip.conf
                sipconf.write(mysipconf1.format(dict[user].Name) + '\n')
                sipconf.write(mysipconf2.format(dict[user].Passw) + '\n')
                if dict[user].Mailbox != "None":
                    sipconf.write(mysipconf3.format(dict[user].Mailbox) + '\n')
                sipconf.write('\n')
                ## my-localusers.conf
                if dict[user].Number != "None":
                    usersconf.write(mylocalus1.format(dict[user].Name, dict[user].Number) + '\n')
                usersconf.write(mylocalus2.format(dict[user].Name) + '\n')
                usersconf.write(mylocalus3.format(dict[user].Name) + '\n')
                usersconf.write(mylocalus4.format(dict[user].Name) + '\n')
                usersconf.write('\n')


## Writing conf fieles in cicle for each dep
for dep in users_deps_u:
    Wr_conf(dep)

# Close conf files
sipconf.close()
usersconf.close()

### Reload asterisk configaration
cmd1 = "service asterisk reload"
os.system(cmd1)

### Fin
