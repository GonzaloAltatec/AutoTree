import xmlrpc.client

class Odoo:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        #Data from the class
        self.uid = Odoo.login(self)
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        self.search_table = None
        self.req_data = None

    def login(self):
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        uid = common.authenticate(self.db, self.username, self.password, {})
        return(uid)

    def search(self, table, element, operator):
        request = self.models.execute_kw(self.db, self.uid, self.password, table, 'search', [[[element, '=', operator]]])
        self.search_table = table
        self.req_data = request
        return(request)

    def read(self, request):
        read_req = self.models.execute_kw(self.db, self.uid, self.password, self.search_table, 'read', [request])
        return(read_req)