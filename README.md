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
   * my-sip.conf - with sip users id, you shoud include it in standart sip.conf using: "#include /etc/asterisk/my-sip.conf"
   * my-localusers.conf - with dialplans for internal short numbers, it must be included in extention.conf using: "#include /etc/asterisk/my-mylocalusers.conf" , "include > [LocalUsers]"
   
## Run scrip
Do - chmod +x 
Manualy or use cron  to sync it once in 10 minutes for example.
