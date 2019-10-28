import pandas as pd
import numpy as np
import os
from math import sin, cos, sqrt, atan2, radians

class questMap:

    def __init__(self, lat, lng):
        self.file = './lib/map/questMaps.csv'
        self.question_file = './lib/map/question.csv'
        self.lat = lat
        self.lng = lng

    def main(self):
        pins = self.settingMap()
        question = self.settingQuestion(pins=pins)
        return pins, question

    def settingQuestion(self, pins):
        question = {'name':[],'Question':[], 'A':[], 'B':[], 'C':[], 'Answer':[],'copyRight':[], 'explanation':[]}
        df = pd.read_csv(self.question_file)
        for name in pins['name']:
            question['name'].append(name)
            question['Question'].append(list(df[df['name'] == name]['Question'])[0])
            question['A'].append(list(df[df['name'] == name]['A'])[0])
            question['B'].append(list(df[df['name'] == name]['B'])[0])
            question['C'].append(list(df[df['name'] == name]['C'])[0])
            question['Answer'].append(list(df[df['name'] == name]['Answer'])[0])
            question['copyRight'].append(list(df[df['name'] == name]['copyRight'])[0])
            question['explanation'].append(list(df[df['name'] == name]['explanation'])[0])
        return question
            


    def settingMap(self):
        pins = {'name':[],'lat':[], 'lng':[], 'icon':[]}
        maps = pd.read_csv(self.file)
        for index in range(len(maps)):
            lat = list(maps.ix[[index],['lat']]['lat'])[0]
            lng = list(maps.ix[[index],['lng']]['lng'])[0]
            name = list(maps.ix[[index],['name']]['name'])[0]
            distance = self.distancePoint(lat=lat, lng=lng)
            print(name,':', distance)
            if distance < 1:
                flg = '00'
                pins['name'].append(name)
                pins['lat'].append(lat)
                pins['lng'].append(lng)
                pins['icon'].append(str(flg))
            else:
                flg = '01'
                pins['name'].append(name)
                pins['lat'].append(lat)
                pins['lng'].append(lng)
                pins['icon'].append(str(flg))
        return pins

    def distancePoint(self, lat, lng):
        R = 6373.0
        lat1 = radians(self.lat)
        lon1 = radians(self.lng)
        lat2 = radians(lat)
        lon2 = radians(lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
