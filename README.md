# aster-sync-users
Thise scrypt create sip users from data in mysql.
You will need a table with users parameters, in coloums:
  * sip_id - username
  * depName - easy to separate users
  * Sip_Pass - password for sip acc
  * Sip_Number - short number, for internal use
  * Sip_Mailbox - voise mailbox
  
  ## Script will read data from DB
  It will create two conf files:
  
