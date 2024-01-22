class CA:
    def __init__(self, name, ip, vca, esp):
        self.name = name
        self.ip = ip
        self.vca = vca
        self.esp = esp
   
    def dic(self):
        ccaa = {
            "Nombre": self.name,
            "IP": self.ip,
            "VCA IP": self.vca,
            "ESP IP": self.esp
        }
        return(ccaa)