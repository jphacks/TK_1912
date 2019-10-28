import pandas as pd
import os

# 指定された場所に関する出題文や選択肢といったデータを返却する
class AnswerManage:

    def __init__(self, area):
        self.area = area
    
    def acquisitionQuest(self):
        df = pd.read_csv('./lib/map/question.csv', index_col=False)
        # 指定した場所の行を取得
        areaDF = df[df['name'] == self.area]
        # dataframeをjson形式に変更
        data = {}
        for i in areaDF.columns:
            data[i] = list(areaDF[i])[0]
        return data
