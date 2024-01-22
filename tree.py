import odoo
from elements import CA

class OdooTree:
    def __init__(self, id):
        self.element = id
        self.elements = odoo.installation(id)
        self.cacp_qty = int(self.elements['CACP'][1])
        self.cacv_qty = int(self.elements['CACV'][1])

    def nvr_tree(self):
        nvr_qty = int(self.elements["Nvr"][1])
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
        
    def camera_tree(self):
        cam_qty = int(self.elements["Cameras"][1])
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
    
    def ccaa_dictionary(self):
        total = self.cacp_qty + self.cacv_qty
        name = self.ccaa_names()
        ip = self.ccaa_ip()
        vca = self.vca_ip()
        esp = self.esp_ip()

        ca_dict = {}

        for x in range(total):
            ca = CA(name[x], ip[x], vca[x], esp[x])
            ca_values = ca.dic()
            ca_dict[f'CA{x+1}'] = ca_values
        return(ca_dict)