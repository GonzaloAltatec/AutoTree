from odoo import Odoo
from re import split
import os
import json

class Tree:
    def __init__(self, id):
        self.id = id
        self.erp = Tree.requests(self)
        self.elements = Tree.ins_elements(self)
        self.cacp_qty = int(self.elements['CACP'])
        self.cacv_qty = int(self.elements['CACV'])
        self.net = Tree.network(self)
        self.password = Tree.ins_password(self)

    def requests(self):
        act_dir = os.path.dirname(__file__)
        dat_dir = os.path.join(act_dir, 'user.json')

        with open(dat_dir, 'r') as usr_file:
            usr_data = json.load(usr_file)
        erp_data = Odoo(usr_data['url'], usr_data['db'], usr_data['username'], usr_data['password'])
        return(erp_data)

    def ins_elements(self):
        #Lectura de ID's de Instalación
        request = self.erp.search('project.project', 'z_numero', self.id)
        request_read = self.erp.read(request)
        
        product_list = ['CVCCV', 'CVCSG', 'CACP', 'CACV', 'CACSS']

        product_dict = {
            'CVCCV': 0,
            'CVCSG': 0,
            'CACP': 0,
            'CACV': 0,
            'CACSS': 0
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

    def ins_password(self):
        sys_request = self.erp.search('project.project', 'z_numero', self.id)
        sys_read = self.erp.read(sys_request)
        for sys in sys_read:
            sys_id = sys['z_sistema_id']
        
        router_request = self.erp.search('altatec.router', 'sistema_id', sys_id[0])
        router_read = self.erp.read(router_request)
        for router in router_read:
            router_password = router['router_password']
        return(router_password)

    def network(self):
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

    def nvr_ip(self):
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

    def nvr_tree(self):
        nvr_list = []
        nvr = {
            'Nombre': '0',
            'Dirección IP': '0',
            'Máscara de Subred': '255.255.255.0',
            'Puerta de enlace': '0',
            'DNS Principal': '8.8.8.8',
            'DNS Secundario': '8.8.4.4',
            'Puerto HTTP': '80',
            'Puerto SDK': '8000',
            'Puerto RTSP': '554',
            'Usuario': 'admin',
            'Password': '0'
        }

        ip = Tree.nvr_ip(self)
        
        for n in range(len(ip)):
            nvr['Nombre'] = f'NVR{n+1}'
            nvr['Dirección IP'] = f'{self.net}{ip[n]}'
            nvr['Puerta de enlace'] = f'{self.net}1'
            nvr['Password'] = f'{self.password}'
            nvr_list.append(nvr.copy())

        if self.elements['CVCSG'] != 0:
            return(nvr_list)
        else:
            return(False)

    def camera_ip(self):
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

    def camera_tree(self):
        ip = Tree.camera_ip(self)
        camera_list = []
        camera = {
            'Nombre': '0',
            'WDR Activado': 'SI/NO',
            'Dirección IP': '0',
            'Puerto HTTP': '80',
            'Puerto SDK': '8000',
            'Puerto RTSP': '554',
            'Usuario': 'admin',
            'Password': '0'
        }

        nvr_num = 1
        cam_num = 1

        for n in range(len(ip)):
            camera['Nombre'] = f'C{cam_num}N{nvr_num}'
            cam_num += 1
            if n == 19:
                nvr_num += 1
                cam_num = 1
            if n == 39:
                nvr_num += 1
                cam_num = 1
            camera['Dirección IP'] = f'{self.net}{ip[n]}'
            camera['Password'] = f'{self.password}'
            camera_list.append(camera.copy())
        return(camera_list)

    def ccaa_type(self):
        if self.cacp_qty >= 1 and self.cacv_qty == 0:
            return('CACP')
        elif self.cacv_qty >= 1 and self.cacp_qty == 0:
            return('CACV')
        elif self.cacp_qty >= 1 and self.cacv_qty >= 1:
            return('CCAA')
        else:
            return('ERROR CCAA')

    def ccaa_names(self):
        ccaa = self.ccaa_type()
        start_count = 1
        name_list = []

        if ccaa == 'CACP':
            self.cacp_qty += 1
            for name in range(1, self.cacp_qty):
                name_list.append(f"CA{name} - PEATONAL")
            return(name_list)
        elif ccaa == 'CACV':
            self.cacv_qty += 1
            for name in range(1, self.cacv_qty):
                name_list.append(f"CA{name} - VEHICULOS")
            return(name_list)
        elif ccaa == 'CCAA':
            ccaa_final = self.cacp_qty + self.cacv_qty +1
            while start_count <= self.cacp_qty:
                name_list.append(f"CA{start_count} - PEATONAL")
                start_count += 1
            while start_count < ccaa_final:
                name_list.append(f"CA{start_count} - VEHICULOS")
                start_count += 1
            return(name_list)

    def ccaa_ip(self):
        ccaa_total = self.cacp_qty + self.cacv_qty
        ip_start = 125
        ip_final = ccaa_total +125 -1
        ip_list = [125]

        while ip_final > ip_list[-1]:
            ip_start += 1
            ip_list.append(ip_start)
        return(ip_list)

    def vca_ip(self):
        ccaa_total = self.cacp_qty + self.cacv_qty    
        ip_start = 165
        ip_final = ccaa_total +165 -1
        ip_list = [165]

        while ip_final > ip_list[-1]:
            ip_start += 1
            ip_list.append(ip_start)
        return(ip_list)
    
    def esp_ip(self):
        ccaa_total = self.cacp_qty + self.cacv_qty
        ip_start = 205
        ip_final = ccaa_total +205 -1
        ip_list = [205]

        while ip_final > ip_list[-1]:
            ip_start += 1
            ip_list.append(ip_start)
        return(ip_list)
        
    def ccaa_tree(self):
        total_ca = self.cacp_qty + self.cacv_qty
        name = self.ccaa_names()
        ip = self.ccaa_ip()
        vca = self.vca_ip()
        esp = self.esp_ip()

        sys_request = self.erp.search('project.project', 'z_numero', self.id)
        sys_read = self.erp.read(sys_request)
        for sys in sys_read:
            sys_id = sys['z_sistema_id']


        caa_list = []

        cacp = {
            'Nombre': '0',
            'Dirección IP': '0',
            'Usuario': 'admin',
            'Password': '0',
            'ESP32 IP': '0',
            'ESP32 MAC': '0',
            'VCA Nombre': '0',
            'VCA IP': '0',
            'VCA Usuario': 'admin',
            'VCA Password': '0',
            'VCA HTTP': '80',
            'VCA SDK': '8000',
            'VCA RTSP': '554',
            'Lector Proximidad': '0',
            'Password Ralset': '0'
        }

        cacv = {
            'Nombre': '0',
            'Dirección IP': '0',
            'Usuario': 'admin',
            'Password': '0',
            'ESP32 IP': '0',
            'ESP32 MAC': '0',
            'VCA Nombre': '0',
            'VCA IP': '0',
            'VCA Usuario': 'admin',
            'VCA Password': '0',
            'VCA HTTP': '80',
            'VCA SDK': '8000',
            'VCA RTSP': '554',
            'Via Radio Canal': '1',
            'Via Radio Reader': '1',
            'Lector Proximidad 1': '0',
            'Lector Proximidad 2': '0',
            'Password Ralset': '0'
        }

        for ca in range(total_ca):
            position = name[ca].find('- PEATONAL')
            if position != -1:
                cacp['Nombre'] = name[ca]
                cacp['Dirección IP'] = f'{self.net}{ip[ca]}'
                cacp['Password'] = f'{self.password}'
                cacp['ESP32 IP'] = f'{self.net}{esp[ca]}'
                cacp['VCA Nombre'] = f'V{ca+1}CA{ca+1}'
                cacp['VCA IP'] = f'{self.net}{vca[ca]}'
                cacp['Lector Proximidad'] = f'LP{ca+1}'
                cacp['Password Ralset'] = f'Ralset-{sys_id[0]}'
                caa_list.append(cacp.copy())
            else:
                cacv['Nombre'] = name[ca]
                cacv['Dirección IP'] = f'{self.net}{ip[ca]}'
                cacv['Password'] = f'{self.password}'
                cacv['ESP32 IP'] = f'{self.net}{ip[ca]}'
                cacv['VCA Nombre'] = f'V{ca+1}CA{ca+1}'
                cacv['VCA IP'] = f'{self.net}{vca[ca]}'
                cacv['Lector Proximidad 1'] = f'LP{ca+1}'
                cacv['Lector Proximidad 2'] = f'LP{ca+2}'
                cacv['Password Ralset'] = f'Ralset-{sys_id[0]}'
                caa_list.append(cacv.copy())

        return(caa_list)

    def sec_room(self):
        hub = {
            'Nº de Abonado': '',
            'Dirección IP': 'DHCP',
            'Usuario Admin': 'admin',
            'Identificador del Hub': '0',
            'Código Teclado': '0',
            'Código Coacción': '0'
        }
        teclado = {
            'Nº Zona': '1',
            'Identificativo': 'TECLADO',
            'Tipo': 'Tecnica',
            'Cámara Asociada': '',
            'Descripción': 'Teclado',
            'Grupo': '1'
        }
        sirena = {
            'Nº Zona': '2',
            'Identificativo': 'SIRENA',
            'Tipo': 'Tecnica',
            'Cámara Asociada': '',
            'Descripción': 'Sirena',
            'Grupo': '1'
        }
        puerta = {
            'Nº Zona': '3',
            'Identificativo': 'PUERTA DEL CUARTO',
            'Tipo': 'Tecnica',
            'Cámara Asociada': '',
            'Descripción': 'Magnético del Cuarto',
            'Grupo': '1'
        }
        sismico = {
            'Nº Zona': '4',
            'Identificativo': 'SISMICO DEL CUARTO',
            'Tipo': 'Tecnica',
            'Cámara Asociada': '',
            'Descripción': 'Sismico del Cuarto',
            'Grupo': '1'
        }
        detector = {
            'Nº Zona': '5',
            'Identificativo': 'DETECTOR DEL CUARTO',
            'Tipo': 'Retardada',
            'Cámara Asociada': 'Fotodetector',
            'Descripción': 'Fotodetector del Cuarto',
            'Grupo': '1'
        } 
        return(hub, teclado, sirena, puerta, sismico, detector)

    def run(self):
        id_input = input('[+] Introduce ID de Instalación: ')
        tree = Tree(id_input)

        elements_tree = []
        elements_tree.append(tree.nvr_tree())
        elements_tree.append(tree.camera_tree())
        elements_tree.append(tree.ccaa_tree())
        elements_tree.append(tree.sec_room())

        return(elements_tree)