import pandas as pd
import numpy as np
import os

class Management:

    def __init__(self, user_id, password):
        self.user = user_id
        self.password = password
        self.file_name = './lib/User/userManagement.csv'

    def signup(self):
        if os.path.exists(self.file_name):
            df = pd.read_csv(self.file_name)
            users = list(df['User'])
            passwords = list(df['Password'])
            if self.user in users:
                flg = False
            else:
                self.registration(user=users, password=passwords)
                flg = True
        else:
            self.registration(user=[], password=[])
            flg = True
        return flg

    def checkLogin(self):
        if os.path.exists(self.file_name):
            df = pd.read_csv(self.file_name)
            flg = self.checkUserPassword(df=df)
            return flg
        else:
            return False
    
    def save_data(self, df):
        df.to_csv(self.file_name,index=False)

    def registration(self, user, password):
        user.append(self.user)
        password.append(self.password)
        data = np.array([user, password]).T
        print('siginup;', data)
        df = pd.DataFrame(data=data, columns=['User','Password'])
        self.save_data(df=df)
    
    def checkUserPassword(self, df):
        users = list(df['User'])
        if self.user in users:
            password = list(df[df['User'] == self.user]['Password'])[0]
            if password == self.password:
                return True
            else:
                return False
        else:
            return False
