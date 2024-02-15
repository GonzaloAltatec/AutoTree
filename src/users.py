import json
import os

class User:
    def __init__(self, user):
        self.user = user

    def select(self):
        act_dir = os.path.dirname(__file__)
        dat_dir = os.path.join(act_dir, 'user.json')

        with open(dat_dir, 'r') as usr_file:
            usr_data = json.load(usr_file)
        return(usr_data[self.user])