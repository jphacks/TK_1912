import pandas as pd
import os

class AnswerManage:

    def __init__(self, area):
        self.area = area
    
    def acquisitionQuest(self):
        df = pd.read_csv('./lib/map/question.csv', index_col=False)
        areaDF = df[df['name'] == self.area]
        data = {}
        for i in areaDF.columns:
            data[i] = list(areaDF[i])[0]
        return data
