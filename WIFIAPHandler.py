from WIFIAP import WIFIAP
import socket
import json
import time
import glob
import re
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class WIFIAPHandler():
    def __init__(self):
        self.ESSIDList = []
        self.BSSIDDict = {}
        self.ESSIDDict = {}
        self.fileslist = []
        self.read_from_files()
        
    
    def parse_line(self,line):
        fields = line.split(';')
        if len(fields) < 38:
            raise Exception("Bad format for AP")

        try:
            first_time = datetime.strptime(fields[19], '%a %b %d %H:%M:%S %Y')
        except:
            first_time = datetime(1970, 1, 1)

        try:
            last_time = datetime.strptime(fields[19], '%a %b %d %H:%M:%S %Y')
        except:
            last_time = datetime(1970, 1, 1)
        return WIFIAP(
            fields[1],
            fields[2],
            fields[3],
            fields[4],
            fields[5],
            fields[6],
            fields[7],
            fields[8],
            fields[9],
            fields[10],
            fields[11],
            fields[12],
            fields[13],
            fields[14],
            fields[15],
            fields[16],
            fields[17],
            fields[18],
            first_time,
            last_time,
            fields[21],
            fields[22],
            fields[23],
            float(fields[24]),
            float(fields[25]),
            float(fields[26]),
            float(fields[27]),
            float(fields[28]),
            float(fields[29]),
            float(fields[30]),
            float(fields[31]),
            float(fields[32]),
            float(fields[33]),
            float(fields[34]),
            fields[35],
            fields[36],
            fields[37],
        )

    def getListByESSID(self,ESSID):
        ESSID.strip()
        to_json = []
        candidates = process.extract(ESSID, self.ESSIDList)
        for candidate in candidates:
            bssid_list = self.ESSIDDict[candidate[0]]
            
            for bssid in bssid_list:
                wifiap = self.BSSIDDict[bssid]
                to_json.insert(0,wifiap.getHTML())
        
        return json.dumps(to_json)

    def update_from_file(self,file):
        with open(file,'r',encoding = "ISO-8859-1") as f:
            self.fileslist.append(file)
            lines = f.readlines()
        for line in lines:
            try:
                wifiap = self.parse_line(line)
                if wifiap.ESSID not in self.ESSIDList and wifiap.ESSID != '':
                    self.ESSIDList.append(wifiap.ESSID)
                if wifiap.BSSID in self.BSSIDDict:
                    self.BSSIDDict[wifiap.BSSID].update(wifiap)
                else:
                    self.BSSIDDict[wifiap.BSSID]=wifiap
                if wifiap.ESSID in self.ESSIDDict:
                    if wifiap.BSSID not in self.ESSIDDict[wifiap.ESSID]:
                        self.ESSIDDict[wifiap.ESSID].append(wifiap.BSSID)
                else:
                    self.ESSIDDict[wifiap.ESSID] = [wifiap.BSSID]
            except Exception as e: # work on python 2.x
                print(e)
    
    def read_from_files(self):
        path = './kismet/*'
        files = glob.glob(path)
        for file in files:
            with open(file,'r',encoding = "ISO-8859-1") as f:
                self.fileslist.append(file)
                lines = f.readlines()
            for line in lines:
                try:
                    wifiap = self.parse_line(line)
                    if wifiap.ESSID not in self.ESSIDList and wifiap.ESSID != '':
                        self.ESSIDList.append(wifiap.ESSID)
                    if wifiap.BSSID in self.BSSIDDict:
                        self.BSSIDDict[wifiap.BSSID].update(wifiap)
                    else:
                        self.BSSIDDict[wifiap.BSSID]=wifiap
                    if wifiap.ESSID in self.ESSIDDict:
                        if wifiap.BSSID not in self.ESSIDDict[wifiap.ESSID]:
                            self.ESSIDDict[wifiap.ESSID].append(wifiap.BSSID)
                    else:
                        self.ESSIDDict[wifiap.ESSID] = [wifiap.BSSID]
                except Exception as e: # work on python 2.x
                    print(e)