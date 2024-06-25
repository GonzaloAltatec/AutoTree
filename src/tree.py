#Versión 9.2
#CAMBIAR .odoo_api antes de enviar
from odoo_api import Odoo
from re import split
import os
import json
import secrets
from string import digits, ascii_letters

class Tree:
    def __init__(self, id = False, production = False, usr_data = None):  
        self.id = id
        self.production = production
        self.usr_data = usr_data
        self.erp = self.requests()
        self.elements = self.ins_elements()
        self.total_ca = int(self.elements['CACP'] + self.elements['CACP1'] + self.elements['CACV'] + self.elements['CACV1'] + self.elements['CCAASC'])
        self.net = self.network()
        self.password = self.ins_password()
        self.cra_pass = self.generate_pass()
        if not self.id:
            id_input = input('[+] Introduce ID de Instalación: ')
            self.id = id_input
        
    def requests(self):
        if not self.production:   
            act_dir = os.path.dirname(__file__)
            dat_dir = os.path.join(act_dir, 'user.json')
            with open(dat_dir, 'r') as usr_file:
                usr_data = json.load(usr_file)
        else:
            usr_data = self.usr_data   
        erp_data = Odoo(usr_data['url'], usr_data['db'], usr_data['username'], usr_data['password'])
        return(erp_data)

    def ins_elements(self): #Saca un diccionario con la cantidad de elementos de cada tipo
        #Lectura de ID's de Instalación
        request = self.erp.search('project.project', 'z_numero', self.id)
        request_read = self.erp.read(request)
        
        #Añadir aquí referencia de producto para buscar más elementos
        product_list = ['CVCCV', 'CVCSG', 'CACP', 'CACP1', 'CACV', 'CACV1', 'CACSS', 'CVKP1', 'CVKP2', 'CCAASC', 'CAPA', 'CAPA1']

        #Añadir aquí también
        product_dict = {
            'CVCCV': 0,
            'CVCSG': 0,
            'CACP': 0,
            'CACP1': 0,
            'CACV': 0,
            'CACV1': 0,
            'CACSS': 0,
            'CVKP1': 0,
            'CVKP2': 0,
            'CCAASC': 0,
            'CAPA': 0,
            'CAPA1': 0
        }

        #Preparamos una lista con el campo de ID's de la lectura de Instalación
        for x in request_read:
            elem_id = x['z_equipo_ids']

        #Hacemos un bucle sobre los diferentes tipos de elementos
        #El bucle hace otra llamada a los códigos de productos
        #Seteamos la lista de ID's de instalación y las de productos
        #Iteramos sobre los sets buscando las intersecciones y los ponemos en un diccionario de cantidades
        for product in product_list:
            elem_req = self.erp.search('sale.order.line', 'product_id.default_code', product)
            elem_list = set(elem_req)
            id_list = set(elem_id)
            rep_elem = id_list.intersection(elem_list)
            if rep_elem:
                ins_list = list(rep_elem)
                ins_list_read = self.erp.read(ins_list) 
                for y in ins_list_read:
                    ins_num = int(y['product_uom_qty'])
                    product_dict[product] = ins_num
        return(product_dict)
       
    def ins_password(self): #Busca la contraseña de la instalación
        sys_request = self.erp.search('project.project', 'z_numero', self.id)
        sys_read = self.erp.read(sys_request)
        for sys in sys_read:
            sys_id = sys['z_sistema_id']
        
        router_request = self.erp.search('altatec.router', 'sistema_id', sys_id[0])
        router_read = self.erp.read(router_request)
        for router in router_read:
            router_password = router['router_password']
        return(router_password)

    def generate_pass(self, length=8): #Generación de contraseña aleatoria para usuario Ralset
        chars = digits + ascii_letters
        return(''.join(secrets.choice(chars) for c in range(length)))

    def network(self): #Lee la IP del Router y define el rango de red a seguir
        sys_request = self.erp.search('project.project', 'z_numero', self.id)
        sys_read = self.erp.read(sys_request)
        for sys in sys_read:
            sys_id = sys['z_sistema_id']
        
        router_request = self.erp.search('altatec.router', 'sistema_id', sys_id[0])
        router_read = self.erp.read(router_request)
        for router in router_read:
            router_ip = router['ip_cctv']
        ip = router_ip.split('.')
        net = str(ip[0] + '.' + ip[1] + '.' + ip[2] + '.') 
        return(net)

    def nvr_ip(self): #Listado con IP de Host de Grabadores
        nvr_qty = int(self.elements['CVCSG'])
        nvr_ip_final = nvr_qty + 10

        nvr_list = [11]
        nvr_ip_inicio = 11

        if nvr_ip_final == 11:
            return(nvr_list)
        elif nvr_ip_final > 11 and nvr_ip_final < 15:
            while nvr_ip_inicio < nvr_ip_final: 
                nvr_ip_inicio += 1
                nvr_list.append(nvr_ip_inicio)
            return(nvr_list)
        elif nvr_ip_final == 15:
            while nvr_ip_inicio < nvr_ip_final: 
                nvr_ip_inicio += 1
                nvr_list.append(nvr_ip_inicio)
            return(nvr_list)
        else:
            return("Cantidad no soportada")

    def nvr_tree(self): #Arbol del "Elemento" NVRx con todas sus propiedades
        nvr_list = []
        nvr = {
            'name': '0',
            'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
            'product_id': 'CVCSG',
            'NOMBRE': '0',
            'DIRECCION IP': '0',
            'MASCARA DE SUBRED': '255.255.255.0',
            'PUERTA DE ENLACE': '0',
            'DNS PRINCIPAL': '8.8.8.8',
            'DNS SECUNDARIO': '8.8.4.4',
            'PUERTO HTTP': '80',
            'PUERTO SDK': '8000',
            'PUERTO RTSP': '554',
            'USUARIO': 'admin',
            'PASSWORD': '0'
        }

        ip = Tree.nvr_ip(self)
        
        for n in range(len(ip)):
            nvr['name'] = f'NVR{n+1}'
            nvr['NOMBRE'] = f'NVR{n+1}'
            nvr['DIRECCION IP'] = f'{self.net}{ip[n]}'
            nvr['PUERTA DE ENLACE'] = f'{self.net}1'
            nvr['PASSWORD'] = f'{self.password}'
            nvr_list.append(nvr.copy())

        if self.elements['CVCSG'] != 0:
            return(nvr_list)
        else:
            return(False)

    def camera_ip(self): #Listado de las IP de Host de las Cámaras
        cam_qty = int(self.elements['CVCCV'])
        cam_ip_final = cam_qty + 16 -1

        cam_list = [16]
        cam_ip_inicio = 16

        if cam_ip_final == 16:
            return(cam_list)
        elif cam_ip_final > 16 and cam_ip_final < 120:
            while cam_ip_inicio < cam_ip_final: 
                cam_ip_inicio += 1
                cam_list.append(cam_ip_inicio)
            return(cam_list)
        elif cam_ip_final == 120:
            while cam_ip_inicio < cam_ip_final: 
                cam_ip_inicio += 1
                cam_list.append(cam_ip_inicio)
            return(cam_list)
        else:
            return("Cantidad no soportada")

    def camera_tree(self): #Arbol del "Elemento" CxNx con todas las propiedades
        ip = Tree.camera_ip(self)
        camera_list = []
        camera = {
            'name': '0',
            'parent_id': '',
            'product_id': 'CVCCV',
            'NOMBRE': '0',
            'WDR ACTIVADO': 'SI/NO',
            'DIRECCION IP': '0',
            'PUERTO HTTP': '80',
            'PUERTO SDK': '8000',
            'PUERTO RTSP': '554',
            'USUARIO': 'admin',
            'PASSWORD': '0'
        }

        nvr_num = 1
        cam_num = 1

        for n in range(len(ip)):
            camera['name'] = f'C{cam_num}N{nvr_num}'
            camera['NOMBRE'] = f'C{cam_num}N{nvr_num}'
            camera['parent_id'] = f'NVR{nvr_num}'
            cam_num += 1
            if n == 19:
                nvr_num += 1
                cam_num = 1
            if n == 39:
                nvr_num += 1
                cam_num = 1
            if n == 59:
                nvr_num += 1
                cam_num = 1
            if n == 79:
                nvr_num += 1
                cam_num = 1
            camera['DIRECCION IP'] = f'{self.net}{ip[n]}'
            camera['PASSWORD'] = f'{self.password}'
            camera_list.append(camera.copy())
        if self.elements['CVCCV'] != 0:
            return(camera_list)
        else:
            return(False)
 
    def ccaa_ip(self): #Genera las IP de Host de CCAA
        ip_start = 125
        ip_final = self.total_ca +125 -1
        ip_list = [125]

        while ip_final > ip_list[-1]:
            ip_start += 1
            ip_list.append(ip_start)
        return(ip_list)

    def vca_ip(self): #Genera IP de Host de Cámaras de CCAA (VCA)
        ip_start = 165
        ip_final = self.total_ca +165 -1
        ip_list = [165]

        while ip_final > ip_list[-1]:
            ip_start += 1
            ip_list.append(ip_start)
        return(ip_list)
    
    def esp_ip(self): #Genera IP de Host de ESP32 de CCAA
        ip_start = 205
        ip_final = self.total_ca +205 -1
        ip_list = [205]

        while ip_final > ip_list[-1]:
            ip_start += 1
            ip_list.append(ip_start)
        return(ip_list)
                
    def sec_room(self): #Arbol de "Elemento" Sala de Seguridad (Redefiniendo Producto)
        if self.elements['CACSS'] == 1: 
            ajax = []
            
            hub = {
                'name': 'ALARMA INALAMBRICA',
                'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
                'product_id': 'CACSS',
                'NUMERO ABONADO': '',
                'FABRICANTE': 'AJAX',
                'MODELO': 'HUB 2 (2G)',
                'UBICACION': '',
                'ID': '0',
                'CODIGO USUARIO': '0',
                'CODIGO COACCION': '0',
                'CODIGO INSTALADOR': '0'
            }
            transmisor_1 = {
                'name': 'TRANSMISOR PRINCIPAL',
                'parent_id': 'ALARMA INALAMBRICA',
                'TIPO': 'ETHERNET',
                'MODELO': 'INTEGRADO',
                'DIRECCION IP': f'{self.net}100',
                'PUERTO HTTP': '',
                'PUERTO SOFTWARE': '',
                'PASSWORD MODULO': '',
                'ID SITE PARADOXMYHOME': ''
            }
            transmisor_2 = {
                'name': 'TRANSMISOR SECUNDARIO',
                'parent_id': 'ALARMA INALAMBRICA',
                'TIPO': 'GPRS',
                'MODELO': 'INTEGRADO',
                'DIRECCION IP': '',
                'PUERTO HTTP': '',
                'PUERTO SOFTWARE': '',
                'PASSWORD MODULO': '',
                'ID SITE PARADOXMYHOME': ''
            }

            teclado = {
                'name': 'ZONA 1',
                'parent_id': 'ALARMA INALAMBRICA',
                'IDENTIFICATIVO': 'TECLADO',
                'DESCRIPCION': 'SABOTAJE TAPA TECLADO',
                'AREA': '1',
                'TIPO DE DETECTOR': 'SABOTAJE DISPOSITIVO',
                'TIPO DE ZONA': '',
                'CAMARA ASOCIADA': '',
                'CONECTADA A': 'HUB'
            }
            sirena = {
                'name': 'ZONA 2',
                'parent_id': 'ALARMA INALAMBRICA',
                'IDENTIFICATIVO': 'SIRENA',
                'DESCRIPCION': 'SABOTAJE TAPA SIRENA',
                'AREA': '1',
                'TIPO DE DETECTOR': 'SABOTAJE DISPOSITIVO',
                'TIPO DE ZONA': '',
                'CAMARA ASOCIADA': '',
                'CONECTADA A': 'HUB'
            }
            puerta = {
                'name': 'ZONA 3',
                'parent_id': 'ALARMA INALAMBRICA',
                'IDENTIFICATIVO': 'PUERTA DEL CUARTO',
                'DESCRIPCION': 'APERTURA PUERTA CUARTO',
                'AREA': '1',
                'TIPO DE DETECTOR': 'CONTACTO MAGNETICO',
                'TIPO DE ZONA': 'RETARDADA',
                'CAMARA ASOCIADA': '',
                'CONECTADA A': 'HUB'
            }
            sismico = {
                'name': 'ZONA 4',
                'parent_id': 'ALARMA INALAMBRICA',
                'IDENTIFICATIVO': 'SISMICO DEL CUARTO',
                'DESCRIPCION': 'SISMICO DEL CUARTO',
                'AREA': '1',
                'TIPO DE DETECTOR': 'DETECTOR IMPACTO',
                'TIPO DE ZONA': 'INSTANTANEA',
                'CAMARA ASOCIADA': 'HUB'
            }
            detector = {
                'name': 'ZONA 5',
                'parent_id': 'ALARMA INALAMBRICA',
                'IDENTIFICATIVO': 'DETECTOR DEL CUARTO',
                'DESCRIPCION': 'DETECTOR VOLUMETRICO DEL CUARTO',
                'AREA': '1',
                'TIPO DE DETECTOR': 'FOTODETECTOR',
                'TIPO DE ZONA': 'INSTANTANEA',
                'CAMARA ASOCIADA': '',
                'CONECTADA A': 'HUB'
            }

            ajax.append(hub)
            ajax.append(transmisor_1)
            ajax.append(transmisor_2)
            ajax.append(teclado)
            ajax.append(sirena)
            ajax.append(puerta)
            ajax.append(sismico)
            ajax.append(detector)

            #Cambios en "Sala de seguridad" en caso de tener CCAA
            if self.total_ca >= 1:
                multi = {
                    'name': '0',
                    'parent_id': 'ALARMA INALAMBRICA',
                    'product_id': 'CAPA',
                    'IDENTIFICATIVO': 'MULTITRANSMITTER',
                    'DESCRIPCION': 'MULTITRANSMITTER',
                    'AREA': '1',
                    'TIPO DE DETECTOR': 'SABOTAJE TAPA MULTITRANSMITTER',
                    'TIPO DE ZONA': '',
                    'CAMARA ASOCIADA': '',
                    'CONECTADA A': 'HUB'
                }

                ca = {
                    'name': '0',
                    'parent_id': 'ALARMA INALAMBRICA',
                    'IDENTIFICATIVO': '',
                    'DESCRIPCION': 'APERTURA FORZADA',
                    'AREA': '2',
                    'TIPO DE DETECTOR': '',
                    'TIPO DE ZONA': 'INSTANTANEA',
                    'CAMARA ASOCIADA': '',
                    'CONECTADA A': 'MULTITRANSMITTER'
                }
                
                multi_counter = 0

                #Generación de elemento "Multitransmitter" en "Sala de Seguridad" en caso de existir CCAA's
                if self.total_ca <= 16:
                    multi['name'] = 'ZONA 6'
                    ajax.append(multi.copy())
                                                        
                elif self.total_ca >= 17 and self.total_ca <= 32:
                    multi['name'] = 'ZONA 6'
                    ajax.append(multi.copy())

                    multi['name'] = 'ZONA 7'
                    ajax.append(multi.copy())
                    multi_counter += 1

                elif self.total_ca >= 33 and self.total_ca <= 39:
                    multi['name'] = 'ZONA 6'
                    ajax.append(multi.copy())

                    multi['name'] = 'ZONA 7'
                    ajax.append(multi.copy())

                    multi['name'] = 'ZONA 8'
                    ajax.append(multi.copy())
                    multi_counter += 2
                else:
                    pass

            for c in range(self.total_ca):
                ca['name'] = f'ZONA {c+multi_counter+7}'
                ca['IDENTIFICATIVO'] = f'CA{c+1}'
                ca['CAMARA ASOCIADA'] = f'V{c+1}CA{c+1}'
                ajax.append(ca.copy())
   

            return(ajax)
        else:
            return(False)

    def kit_portal(self): #Arbol de generación para "Kit Portal" de 1 o 2 cámaras
        if self.elements['CVKP1'] or self.elements['CVKP2'] == 1:
            portal = []
            if self.elements['CVKP1'] == 1:
                c1 = {
                    'name': 'C1',
                    'parent_id': 'ROUTER PARA PORTAL PROTEGIDO',
                    'product_id': 'CVKP1',
                    'NOMBRE': 'C1',
                    'WDR ACTIVADO': 'SI/NO',
                    'DIRECCION IP': 0,
                    'PUERTO HTTP': 80,
                    'PUERTO SDK': 8000,
                    'PUERTO RTSP': 554,
                    'USUARIO': 'admin',
                    'PASSWORD': ''
                }
                
                c1['DIRECCION IP'] = f'{self.net}16'
                c1['PASSWORD'] = f'{self.password}'
                portal.append(c1)

            elif self.elements['CVKP2'] == 1:
                c1 = {
                    'name': 'C1',
                    'parent_id': 'ROUTER PARA PORTAL PROTEGIDO',
                    'product_id': 'CVKP2',
                    'NOMBRE': 'C1',
                    'WDR ACTIVADO': 'SI/NO',
                    'DIRECCION IP': 0,
                    'PUERTO HTTP': 80,
                    'PUERTO SDK': 8000,
                    'PUERTO RTSP': 554,
                    'USUARIO': 'admin',
                    'PASSWORD': ''
                }
                c2 = {
                    'name': 'C2',
                    'parent_id': 'ROUTER PARA PORTAL PROTEGIDO',
                    'product_id': 'CVKP2',
                    'NOMBRE': 'C2',
                    'WDR ACTIVADO': 'SI/NO',
                    'DIRECCION IP': 0,
                    'PUERTO HTTP': 80,
                    'PUERTO SDK': 8000,
                    'PUERTO RTSP': 554,
                    'USUARIO': 'admin',
                    'PASSWORD': ''
                }
                c1['DIRECCION IP'] = f'{self.net}16'
                c1['PASSWORD'] = f'{self.password}'
                c2['DIRECCION IP'] = f'{self.net}17'
                c2['PASSWORD'] = f'{self.password}'
                portal.append(c1)
                portal.append(c2)

            return(portal)                
        else:
            return(False)
     
    def ccaa_tree(self): #Función testing para arbol CCAA
        #---------
        #Variables
        #---------
        cacp_qty = int(self.elements['CACP'])
        cacv_qty = int(self.elements['CACV'])
        cacp1_qty = int(self.elements['CACP1'])
        cacv1_qty = int(self.elements['CACV1'])
        casc_qty = int(self.elements['CCAASC'])
        ip = self.ccaa_ip()
        esp = self.esp_ip()
        vca = self.vca_ip()

        #----------------------------
        #Listas de elementos de arbol
        #----------------------------

        ccaa_list = []

        cacp = {
            'name': '0',
            'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
            'product_id': 'CACP',
            'DIRECCION IP': '0',
            'USUARIO': 'admin',
            'PASSWORD': '0',
            'ESP32 IP': '0',
            'ESP32 MAC': '0',
            'VCA NOMBRE': '0',
            'VCA IP': '0',
            'VCA USUARIO': 'admin',
            'VCA PASSWORD': '0',
            'VCA HTTP': '80',
            'VCA SDK': '8000',
            'VCA RTSP': '554',
            'LECTOR PROXIMIDAD': '0',
            'USUARIO RALSET': 'RALSET',
            'PASSWORD RALSET': '0'
        }
        
        cacv = {
            'name': '0',
            'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
            'product_id': 'CACV',
            'DIRECCION IP': '',
            'USUARIO': 'admin',
            'PASSWORD': '0',
            'ESP32 IP': '0',
            'ESP32 MAC': '0',
            'VCA NOMBRE': '0',
            'VCA IP': '0',
            'VCA USUARIO': 'admin',
            'VCA PASSWORD': '0',
            'VCA HTTP': '80',
            'VCA SDK': '8000',
            'VCA RTSP': '554',
            'VIA RADIO CANAL': '1',
            'VIA RADIO READER': '1',
            'LECTOR PROXIMIDAD 1': '0',
            'LECTOR PROXIMIDAD 2': '0',
            'USUARIO RALSET': 'RALSET',
            'PASSWORD RALSET': '0'
        }
        
        casc = {
            'name': '0',
            'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
            'product_id': 'CCAASC',
            'DIRECCION IP': '0',
            'USUARIO': 'admin',
            'PASSWORD': '0',
            'ESP32 IP': '0',
            'ESP32 MAC': '0',
            'LECTOR PROXIMIDAD': '0'
        }

        #---------------------
        #Modificación de datos
        #---------------------

        counter = 0
        lp_counter = 0

        #Arbol CCAA Peatonal    
        if self.elements['CACP'] or self.elements['CACP1'] != 0:
            for cap in range(cacp_qty + cacp1_qty):
                counter += 1
                if cap >= cacp_qty:
                    cacp['product_id'] = 'CACP1'
                cacp['name'] = f'CA{counter} - PEATONAL'
                cacp['DIRECCION IP'] = f'{self.net}{ip[cap]}'
                cacp['PASSWORD'] = self.password
                cacp['ESP32 IP'] = f'{self.net}{esp[cap]}'
                cacp['VCA NOMBRE'] = f'V{counter}CA{counter}'
                cacp['VCA IP'] = f'{self.net}{vca[cap]}'
                cacp['VCA PASSWORD'] = self.password
                cacp['LECTOR PROXIMIDAD'] = f'LP{counter}'
                lp_counter += 1
                cacp['PASSWORD RALSET'] = self.cra_pass
                ccaa_list.append(cacp.copy())

        #Arbol CCAA Vehiculos        
        if self.elements['CACV'] or self.elements['CACV1'] != 0:
            for cav in range(cacv_qty + cacv1_qty):
                counter += 1
                if cav >= cacv_qty:
                    cacv['product_id'] = 'CACV1'
                cacv['name'] = f'CA{counter} - VEHICULOS'
                cacv['DIRECCION IP'] = f'{self.net}{ip[counter-1]}'
                cacv['PASSWORD'] = self.password
                cacv['ESP32 IP'] = f'{self.net}{esp[counter-1]}'
                cacv['VCA NOMBRE'] = f'V{counter}CA{counter}'
                cacv['VCA IP'] = f'{self.net}{vca[counter-1]}'
                cacv['VCA PASSWORD'] = self.password
                cacv['LECTOR PROXIMIDAD 1'] = f'LP{lp_counter+1}'
                cacv['LECTOR PROXIMIDAD 2'] = f'LP{lp_counter+2}'
                lp_counter += 2
                cacv['PASSWORD RALSET'] = self.cra_pass
                ccaa_list.append(cacv.copy())

        #Arbol CCAA Ascensore 
        if self.elements['CCAASC'] != 0:
            for cas in range(casc_qty):
                counter += 1
                casc['name'] = f'CA{counter} - ASCENSORES'
                casc['DIRECCION IP'] = f'{self.net}{ip[counter-1]}'
                casc['PASSWORD'] = self.password
                casc['ESP32 IP'] = f'{self.net}{esp[counter-1]}'
                casc['LECTOR PROXIMIDAD'] = f'LP{lp_counter}'
                lp_counter += 1
                ccaa_list.append(casc.copy())

        if ccaa_list:
            return(ccaa_list)
        else:
            return(False)

    def capa_tree(self):
        
        capa_list = []

        capa = {
            'name': '',
            'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
            'product_id': 'CAPA',
            'ESP32 IP': '',
            'ESP32 MAC': ''
        }

        capa1 = {
            'name': '',
            'parent_id': 'CCCC - CENTRO DE COMUNICACIONES',
            'product_id': 'CAPA1',
            'ESP32 IP': '',
            'ESP32 MAC': '',
            'NVR IP': ''
        }

        if self.elements['CAPA'] != 0:
            for cap in range(self.elements['CAPA']):
                capa['name'] = f'CAPA {cap+1}'
                capa['ESP32 IP'] = f'{self.net}{5+cap}'
                capa_list.append(capa.copy())
      
        if self.elements['CAPA1'] != 0:
            for cap1 in range(self.elements['CAPA']):
                capa1['name'] = f'CAPA {cap1+1}'
                capa1['ESP32 IP'] = f'{self.net}{5+cap1}'
                capa1['NVR IP'] = f'{self.net}{121+cap1}'
                capa_list.append(capa1.copy())
        
        if capa_list:
            return(capa_list)
        else:
            return(False)

    def run(self): #Ejecuta el arboleador al completo
        
        elements_tree = []
        elements_tree.append(self.nvr_tree())
        elements_tree.append(self.camera_tree())
        elements_tree.append(self.sec_room())
        elements_tree.append(self.capa_tree())
        elements_tree.append(self.ccaa_tree())
        elements_tree.append(self.kit_portal())
        
        return(elements_tree)