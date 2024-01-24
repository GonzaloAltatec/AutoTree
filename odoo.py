from re import split
import sys
sys.path.append('/home/laboratorio/Programs/Odoo')

from odoo_users import User
import odoo_req as Odoo

#Datos de usuario para peticiones a API Odoo
usr = User("gonzalo")
sel_usr = usr.gonzalo()
usr_url = sel_usr["url"]
usr_db = sel_usr["db"]
usr_usr = sel_usr["username"]
usr_pass = sel_usr["password"]

req = Odoo.Request(usr_url, usr_db, usr_usr, usr_pass)

def network(id):
    sys_id = req.get_sys_id(id)
    addr = req.get_router(sys_id)
    net = addr.split('.')
    return(net)

def installation(id):
    elements = req.ins_elements(id)
    return(elements)