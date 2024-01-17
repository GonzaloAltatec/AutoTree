import xmlrpc.client

#Datos de Usuario + UID
url = "https://erp.altatec.es"
db = "altatecsistemas-erp-main-2474910"
username = "gonzalorodriguez@altatec-seguridad.com"
password = "16d7581d0d7b9d871372d3f4062ed5c85c74ee52"
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
common.version()
uid = common.authenticate(db, username, password, {})

#Modelo de peticiones
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

#Testeo de peticiones
request = models.execute_kw(db, uid, password, 'project.project', 'search', [[['z_sistema_id.id', '=', 4470]]])
elements = models.execute_kw(db, uid, password, 'project.project', 'read', [request], {'fields': ['z_equipo_ids']})
cameras_request = models.execute_kw(db, uid, password, 'sale.order.line', 'search', [[['product_id.default_code', '=', 'CVCCV']]])
cameras_list = set(cameras_request)

for x in elements:
    elements_id = x['z_equipo_ids']
    #break
    #print(elements_id)
elements_list = set(elements_id)

repeated_cameras = elements_list.intersection(cameras_list)
cameras_id = list(repeated_cameras)
cameras_read = models.execute_kw(db, uid, password, 'sale.order.line', 'read', [cameras_id])
print(elements)