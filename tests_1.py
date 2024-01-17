import sys
sys.path.append('/home/laboratorio/Programs/Odoo')

from odoo_users import User
import odoo_basic as Odoo

usr = User("gonzalo")
sel_usr = usr.gonzalo()
usr_url = sel_usr["url"]
usr_db = sel_usr["db"]
usr_usr = sel_usr["username"]
usr_pass = sel_usr["password"]

req = Odoo.Request(usr_url, usr_db, usr_usr, usr_pass)

print(req.ins_elements("IN10145"))